#!/bin/bash
# Sentinel Monitor - Universal Linux System Monitor
# Installation Script

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run with sudo"
    exit 1
fi

echo "═══════════════════════════════════════════"
echo "   SENTINEL - System Monitor Installer     "
echo "═══════════════════════════════════════════"
echo ""

# Detect the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "[1/4] Installing dependencies..."
apt-get update -qq
apt-get install -y python3 lm-sensors curl 2>/dev/null || {
    echo "  Note: Some packages may already be installed"
}

echo "[2/4] Configuring sensors..."
# Auto-detect sensors (non-interactive)
yes | sensors-detect 2>/dev/null || sensors-detect --auto 2>/dev/null || echo "  Sensors already configured"

echo "[3/4] Installing Sentinel..."
# Make script executable
chmod +x "$SCRIPT_DIR/sentinel-monitor.py"

# Copy to system bin
cp "$SCRIPT_DIR/sentinel-monitor.py" /usr/local/bin/sentinel
chmod +x /usr/local/bin/sentinel

# Create short alias
ln -sf /usr/local/bin/sentinel /usr/local/bin/sen

echo "[4/4] Setting up shell aliases..."
# Detect user who ran sudo
REAL_USER="${SUDO_USER:-$USER}"
REAL_HOME=$(eval echo ~$REAL_USER)

# Add to user's bashrc if not already present
if ! grep -q "alias sentinel=" "$REAL_HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$REAL_HOME/.bashrc"
    echo "# Sentinel System Monitor aliases" >> "$REAL_HOME/.bashrc"
    echo "alias sentinel='/usr/local/bin/sentinel'" >> "$REAL_HOME/.bashrc"
    echo "alias sen='/usr/local/bin/sentinel'" >> "$REAL_HOME/.bashrc"
    chown $REAL_USER:$REAL_USER "$REAL_HOME/.bashrc"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "✓ Sentinel installed successfully!"
echo "═══════════════════════════════════════════"
echo ""
echo "Usage:"
echo "  sentinel      - Launch Sentinel monitor"
echo "  sen           - Short alias"
echo ""
echo "Controls:"
echo "  q - Quit"
echo "  r - Force refresh"
echo "  i - Check public IP immediately"
echo ""
echo "Features:"
echo "  • Real-time CPU, Memory, Disk monitoring"
echo "  • Live network traffic (KB/s)"
echo "  • Public IP detection"
echo "  • WireGuard status (if configured)"
echo "  • Battery/UPS monitoring (laptops)"
echo "  • CPU frequency warnings"
echo "  • Process tracking"
echo ""
echo "Try it now: sentinel"
echo ""
