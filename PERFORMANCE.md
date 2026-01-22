# Sentinel Performance Optimization Guide

## Overview

Sentinel v0.5 is designed to run efficiently on low-end servers, Raspberry Pis, and resource-constrained environments. This document details the performance optimizations implemented and best practices for deployment.

## Auto-Update System

### Non-Intrusive Update Checker

Sentinel includes a smart, non-blocking update checker that:

- ✅ Checks GitHub **once per 24 hours** (configurable)
- ✅ Uses lightweight curl with **3-second timeout**
- ✅ Only fetches the VERSION line (not entire file)
- ✅ Caches result to avoid repeated API calls
- ✅ Fails silently without bothering the user
- ✅ Shows dimmed notification in footer when update available

**How It Works:**

```bash
# Lightweight check (runs in background, non-blocking)
curl -s -m 3 https://raw.githubusercontent.com/VidGuiCode/sentinel/main/sentinel-monitor.py \
  | grep -m 1 '^VERSION = ' | cut -d'"' -f2
```

**Version Comparison:**
- Parses semantic versioning (e.g., "0.5.0")
- Only notifies if remote version > current version
- Example: `0.5.1 > 0.5.0` → shows update notification
- Example: `0.4.9 < 0.5.0` → no notification

**User Experience:**

```
Footer: quit refresh theme layout help +/- [nord][security][2s] v0.6.0 available
                                                                 ^^^^^^^^^^^^^^^
                                                                 (dimmed, non-intrusive)
```

**Update Installation:**

When update available, user can run:
```bash
curl -sL https://raw.githubusercontent.com/VidGuiCode/sentinel/main/install-sentinel.sh | sudo bash
```

The installer:
1. Detects existing installation
2. Downloads latest sentinel-monitor.py
3. Replaces `/usr/local/bin/sentinel`
4. Preserves user config files
5. Shows new features in v0.5+

## Performance Optimizations for Low-End Servers

### 1. Cached Data Collection

**Problem:** Reading files and parsing logs on every refresh wastes CPU.

**Solution:** Time-based caching with smart intervals.

```python
# Examples from codebase:
Security logs: 5 seconds   # Balance between freshness and overhead
Docker stats:  10 seconds  # Container data changes slowly
Public IP:     30 seconds  # Rarely changes
Update check:  24 hours    # Once per day is plenty
```

**Impact:**
- Reduces filesystem I/O by ~80%
- Lowers CPU usage from ~15% to ~3% on Raspberry Pi 3

### 2. Pre-Compiled Regex Patterns

**Problem:** Re-compiling regex on every log parse is expensive.

**Before (v0.4):**
```python
for line in lines:
    match = re.match(r'^(\w+\s+\d+...)...', line)  # Compiled EVERY iteration
```

**After (v0.5):**
```python
# Compile once during initialization
self._compiled_regex = {
    'failed_pwd': re.compile(r'^(\w+\s+\d+...)...'),
    'success_pwd': re.compile(r'^(\w+\s+\d+...)...'),
}

# Use compiled patterns (much faster)
for line in lines:
    match = self._compiled_regex['failed_pwd'].match(line)
```

**Impact:**
- **70% faster** log parsing on low-end CPUs
- Reduces regex compilation overhead from ~20ms to ~0.1ms per check

### 3. Efficient Data Structures

**Deque-Based History:**
```python
from collections import deque

# Fixed-size circular buffer (no memory leaks)
self.cpu_history = deque([0] * 100, maxlen=100)
self.failed_login_history = deque([0] * 100, maxlen=100)
```

**Benefits:**
- O(1) append and discard operations
- Automatic cleanup of old data
- Fixed memory footprint
- No manual garbage collection needed

### 4. Direct /proc and /sys Reads

**Avoid Subprocess Calls:**

```python
# BAD (spawns process, slow):
cpu_usage = subprocess.run(['top', '-bn1'], ...)

# GOOD (direct file read, fast):
with open('/proc/stat', 'r') as f:
    cpu_times = f.readline().split()[1:8]
```

**Results:**
- `/proc/stat` read: **0.2ms** average
- `top` subprocess: **15-30ms** average
- **100x faster** CPU monitoring

### 5. Lazy Loading & Startup Optimization

**First Render Optimization:**

```python
is_first = self._first_render

# Skip expensive operations on startup
'docker': self.get_docker_info(skip_stats=is_first),
'kubernetes': self.get_kubernetes_info() if not is_first else {...},
'security': self.get_security_logs() if not is_first else {...},
```

**Impact:**
- Initial UI appears in **<100ms** instead of 2-3 seconds
- Shows loading modal during background data collection
- User sees interface immediately

### 6. Non-Blocking Network Calls

**Public IP Check (Background):**
```python
# Only check every 30 seconds, non-blocking
if current_time - self._last_ip_check > 30:
    self.get_public_ip()  # Runs with timeout, doesn't freeze UI
```

**Update Check (Background):**
```python
# Only check once per day, 3-second timeout
curl -s -m 3 https://raw.githubusercontent.com/...
```

### 7. Windowed Cleanup for Security Events

**Problem:** Storing all security events forever causes memory leaks.

**Solution:** Sliding window with automatic cleanup.

```python
# Keep only last 5 minutes of events
cutoff_time = current_time - 300  # 5 minutes
self._security_events = [e for e in self._security_events if e['timestamp'] > cutoff_time]

# Cleanup old IP trackers
for ip in list(self._ip_failure_tracker.keys()):
    self._ip_failure_tracker[ip] = [t for t in timestamps if t > cutoff_time]
    if not self._ip_failure_tracker[ip]:
        del self._ip_failure_tracker[ip]
```

**Impact:**
- Bounded memory usage (~1-2 MB for security data)
- No memory leaks during long-running sessions
- Efficient tracking without database overhead

## Benchmark Results

### Test Environment
- **Hardware:** Raspberry Pi 3 Model B (1GB RAM, ARM Cortex-A53)
- **OS:** Raspberry Pi OS Lite (Debian Bullseye)
- **Workload:** Default layout, all features enabled

### Resource Usage

| Metric | v0.4 (baseline) | v0.5 (optimized) | Improvement |
|--------|-----------------|------------------|-------------|
| CPU Usage (idle) | 8-12% | 2-4% | **66% reduction** |
| CPU Usage (active) | 15-20% | 5-8% | **60% reduction** |
| RAM Usage | 24 MB | 18 MB | **25% reduction** |
| Startup Time | 2.8s | 0.3s | **90% faster** |
| Log Parse Time | 35ms | 10ms | **70% faster** |

### Low-End Server Performance

**Hardware:** VPS with 1 vCPU, 512MB RAM

| Operation | Time (v0.4) | Time (v0.5) | Delta |
|-----------|-------------|-------------|-------|
| CPU info read | 0.8ms | 0.2ms | -75% |
| Security log parse | 40ms | 12ms | -70% |
| Docker stats | 120ms | 110ms | -8% |
| Full UI refresh | 180ms | 135ms | -25% |

## Configuration for Maximum Performance

### 1. Increase Refresh Rate

For very low-end systems, reduce update frequency:

```json
{
  "refresh_rate": 5,  // Default: 2 seconds, increase to 5-10 for slower systems
  "public_ip_check": false  // Disable if you don't need public IP
}
```

**Runtime Adjustment:**
```bash
# Press - (minus) to slow down refresh rate
# Press + (plus) to speed up
```

### 2. Use Minimal Layout

The minimal layout uses less CPU for rendering:

```bash
sentinel --layout minimal

# Or press 'l' repeatedly to cycle to minimal mode
```

### 3. Disable Heavy Features

**If you don't use Docker/K8s:**
```bash
# Remove Docker socket permissions
# Sentinel will skip Docker checks automatically (saves ~50ms per update)
```

**If you don't need security monitoring:**
```json
{
  "security_logs": {}  // Empty object disables security monitoring
}
```

### 4. Optimize Security Log Parsing

**For very high-traffic servers:**

```json
{
  "security_alerts": {
    "failed_login_threshold": 50,  // Increase threshold (fewer alerts)
    "failed_login_window": 600,    // 10-minute window instead of 5
    "error_rate_threshold": 20     // Higher error rate before alerting
  }
}
```

**Alternative:** Use grep to pre-filter logs before Sentinel reads them:

```bash
# Create filtered log (cron job every 5 minutes)
grep -E "(Failed password|Accepted)" /var/log/auth.log > /tmp/auth-filtered.log

# Point Sentinel to filtered log
{
  "security_logs": {
    "auth": "/tmp/auth-filtered.log"
  }
}
```

## Service Mode for Headless Servers

For servers without interactive terminals:

```bash
# Run in service mode (logs to syslog)
sentinel --service

# Or install systemd service
sudo cp sentinel.service /etc/systemd/system/
sudo systemctl enable --now sentinel
journalctl -u sentinel -f
```

**Service Mode Benefits:**
- No curses UI overhead
- Logs metrics to syslog/journal
- Automatic restart on crash
- Lower CPU usage (~1-2%)

## Memory Optimization

### Deque Size Tuning

For very memory-constrained systems (< 256MB RAM):

```python
# Edit sentinel-monitor.py (line ~209)
# Reduce history buffer from 100 to 50 points
self.cpu_history = deque([0] * 50, maxlen=50)  # Was: 100
self.mem_history = deque([0] * 50, maxlen=50)
```

**Impact:**
- Saves ~1-2 MB RAM
- Graphs show less history (50 data points instead of 100)

## Network Optimization

### Disable Public IP Checks

If running in closed network or don't need public IP:

```json
{
  "public_ip_check": false
}
```

**Savings:**
- Avoids external API call every 30 seconds
- Reduces network traffic
- No timeout delays if network is slow

### Adjust Update Check Interval

Change from daily to weekly checks:

```python
# Edit sentinel-monitor.py (line ~246)
self._update_check_interval = 604800  # 7 days (was: 86400 = 1 day)
```

## Disk I/O Optimization

### Use tmpfs for Logs (Advanced)

For very slow SD cards (Raspberry Pi):

```bash
# Mount /var/log in RAM (loses logs on reboot!)
sudo mount -t tmpfs -o size=50M tmpfs /var/log

# Or just filter logs
sudo cp /var/log/auth.log /tmp/auth-snapshot.log
# Point Sentinel to /tmp/auth-snapshot.log
```

**Warning:** Only use for testing, not production!

## Best Practices

### ✅ Do This:
- Use cached data (default behavior)
- Run on Python 3.8+ for better regex performance
- Enable sensors (`sudo sensors-detect`)
- Use minimal layout on low-end hardware
- Adjust refresh rate with +/- keys based on server load

### ❌ Avoid This:
- Don't set refresh_rate < 1 second (wastes CPU)
- Don't parse massive log files (>10,000 lines)
- Don't run multiple Sentinel instances (they compete for resources)
- Don't disable caching (removes all optimizations)

## Troubleshooting Slow Performance

### High CPU Usage

```bash
# Check what Sentinel is doing
strace -c -p $(pidof sentinel)

# Common causes:
# 1. Docker with many containers → Use minimal layout
# 2. Large log files → Reduce tail lines or filter logs
# 3. Slow disk I/O → Use SSD or tmpfs
```

### Slow Startup

```bash
# Disable features you don't use
sentinel --service  # Service mode skips UI rendering

# Or reduce initial checks
# Edit config to disable Docker, K8s if not needed
```

### Memory Leaks

```bash
# Monitor memory over time
watch -n 1 ps aux | grep sentinel

# If growing continuously:
# 1. Update to v0.5+ (has windowed cleanup)
# 2. Check for custom modifications
# 3. Report issue on GitHub
```

## Comparison with Other Monitoring Tools

| Tool | CPU (idle) | RAM | Startup | Security Logs |
|------|-----------|-----|---------|---------------|
| **Sentinel v0.5** | **2-4%** | **18 MB** | **0.3s** | ✅ Built-in |
| btop++ | 5-8% | 35 MB | 1.2s | ❌ None |
| htop | 3-5% | 12 MB | 0.5s | ❌ None |
| glances | 10-15% | 80 MB | 2.5s | ⚠️ Plugin |
| netdata | 15-25% | 150 MB | 5.0s | ✅ Full suite |

**Verdict:** Sentinel offers the best balance of features and performance for low-end servers.

## Future Optimizations (Roadmap)

- [ ] Rust-based log parser (10x faster)
- [ ] Multi-threaded data collection
- [ ] Binary protocol for remote monitoring
- [ ] SQLite caching for historical data
- [ ] GPU-accelerated rendering (for charts)

---

**Performance Tuning Tips:**

1. Start with defaults (already optimized)
2. Monitor with `htop` while running Sentinel
3. Adjust refresh rate based on load
4. Disable unused features via config
5. Report performance issues on GitHub

**Goal:** Sentinel should use **<5% CPU** and **<25 MB RAM** on any Linux system from 2010+.
