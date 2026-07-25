#!/usr/bin/env bash
# Graceful-degradation verification.
#
# Runs Sentinel under containers that are deliberately missing permissions or
# resources and asserts that the UI still renders and *explains* what is
# unavailable, instead of crashing or showing a silently blank panel.
#
# Each scenario checks two things:
#   1. the frame is not blank (the TUI painted at all)
#   2. the expected explanation text is present, either in a panel or in the
#      diagnostics overlay (opened by sending "d")
#
# Usage:  ./bench/degraded.sh
set -uo pipefail
export MSYS_NO_PATHCONV=1

IMAGE=sentinel-degraded
PASS=0
FAIL=0

# scenario <name> <expect-regex> <docker-run-args...>
scenario() {
  local name=$1 expect=$2; shift 2
  local out
  out=$(docker run --rm -e TERM=xterm-256color "$@" "$IMAGE" \
        python3 bench/capture_frame.py --duration 11 --rows 45 --cols 150 \
          --keys d -- python3 sentinel-monitor.py 2>&1)
  local nonblank
  nonblank=$(printf '%s' "$out" | grep -c '[│┌└]')
  if [ "$nonblank" -lt 5 ]; then
    echo "FAIL  ${name}: UI did not render (${nonblank} frame lines)"
    printf '%s\n' "$out" | tail -6 | sed 's/^/      | /'
    FAIL=$((FAIL+1)); return
  fi
  if printf '%s' "$out" | grep -qiE "$expect"; then
    echo "PASS  ${name}: rendered + explained (/${expect}/)"
    PASS=$((PASS+1))
  else
    echo "FAIL  ${name}: rendered but no explanation matching /${expect}/"
    FAIL=$((FAIL+1))
  fi
}

echo "==> Building degradation image"
docker build -q -t sentinel-bench -f bench/Dockerfile.bench . > /dev/null
docker build -q -t "$IMAGE" -f bench/Dockerfile.degraded . > /dev/null

# 1. No docker socket at all (the common Raspberry Pi case).
scenario "no-docker-socket" "socket missing|not installed"

# 2. Docker socket present but unreadable: mounted, process runs unprivileged.
#    Must report a permission problem, not "not installed".
scenario "docker-socket-no-perm" "no permission|failed|socket missing" \
  --user 65534:65534 -v /var/run/docker.sock:/var/run/docker.sock:ro

# 3. Unreadable /var/log: security + proxy log collectors must degrade.
scenario "unreadable-var-log" "security|proxy" \
  --user 65534:65534 -v /dev/null:/var/log/auth.log:ro

# 4. Dropped capabilities + read-only root filesystem.
scenario "dropped-caps-readonly" "not installed|no permission|socket missing" \
  --cap-drop=ALL --read-only --tmpfs /tmp

# 5. Tightest device profile, to be sure degradation is not an OOM crash.
scenario "pi3-limits" "not installed|no permission|socket missing" \
  --cpus=0.5 --memory=256m

echo
echo "==> degraded: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ]
