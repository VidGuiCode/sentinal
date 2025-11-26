# Sentinel v0.4 - Universal Linux System Monitor

A lightweight terminal UI (TUI) system monitor for Linux with real-time graphs, container monitoring, and infrastructure-focused design. Inspired by btop. Optimized for low-power devices.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-0.4.0-cyan.svg)

## Quick start

```bash
curl -sL https://raw.githubusercontent.com/VidGuiCode/sentinal/main/install-sentinel.sh | sudo bash
sentinel
```

## Features

### System Monitoring
- **CPU** - Per-core usage bars, gradient graph, temperature, frequency, governor
- **Memory** - Usage with history graph, available memory tracking
- **Disk** - Mount points with progress bars, Docker volume names & sizes
- **Network** - Live traffic (KB/s), sparkline graphs, VPN status, proxy stats
- **Energy** - RAPL power (desktops), battery stats (laptops)
- **Docker** - Dynamic container list, running/stopped count, volume sizes
- **Kubernetes** - Pod status, node health, failed/pending alerts
- **Processes** - Task count, top CPU/memory consumers
- **Proxy** - Nginx/Caddy traffic monitoring (requests per second)

### v0.4 Features
- **Loading modal** - Shows spinner during initial data load
- **Help overlay** - Press `h` to see all keybindings
- **Adjustable refresh rate** - Press `+`/`-` to speed up or slow down (1-10s)
- **Layout modes** - Press `l` to cycle: default, cpu, network, docker, minimal
- **Dynamic container lists** - Auto-adjusts to available space
- **Improved temperature detection** - Works on ARM, VMs, containers
- **Proxy traffic monitoring** - Shows nginx/caddy requests per second
- **Wider graphs** - 100 data points for full-width terminal graphs
- **Performance optimized** - Fast startup on low-power devices

### Themes
5 built-in color themes (press `t` to cycle):

| Theme | Description |
|-------|-------------|
| `default` | Cyan/green terminal colors |
| `nord` | Arctic, bluish color palette |
| `dracula` | Dark purple/pink theme |
| `gruvbox` | Retro, warm colors |
| `monokai` | Classic editor theme |

Use `--theme <name>` or press `t` in the TUI to switch.

### Alerts
- CPU usage warnings (configurable thresholds)
- Temperature color coding (green/yellow/red)
- Memory pressure indicators
- Battery low warnings
- Docker stopped container alerts
- Kubernetes failed pod alerts

### Network
- Local IP detection
- Public IP detection (cached, non-blocking)
- WireGuard VPN status with peer count
- Real-time traffic graphs
- Total RX/TX statistics
- Reverse proxy traffic (nginx/caddy)

## Installation

### One-Line Install

```bash
curl -sL https://raw.githubusercontent.com/VidGuiCode/sentinal/main/install-sentinel.sh | sudo bash
```

Or with wget:
```bash
wget -qO- https://raw.githubusercontent.com/VidGuiCode/sentinal/main/install-sentinel.sh | sudo bash
```

### From Source

```bash
git clone https://github.com/VidGuiCode/sentinal.git
cd sentinal
sudo bash install-sentinel.sh
```

### Manual (No Installer)

```bash
sudo apt-get install python3 lm-sensors curl
curl -sL https://raw.githubusercontent.com/VidGuiCode/sentinal/main/sentinel-monitor.py | sudo tee /usr/local/bin/sentinel > /dev/null
sudo chmod +x /usr/local/bin/sentinel
```

## Usage

```bash
sentinel                      # Run TUI
sentinel --theme nord         # Use Nord theme
sentinel --service            # Headless service mode
sentinel --init-config        # Create config file
sentinel --help               # Show options
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Force refresh |
| `t` | Cycle themes |
| `l` | Cycle layouts |
| `h` | Toggle help overlay |
| `i` | Check public IP |
| `+` | Faster refresh (min 1s) |
| `-` | Slower refresh (max 10s) |

### Layout Modes

Press `l` to cycle through layouts:
- **default** - Balanced view of all panels
- **cpu** - Emphasize CPU monitoring
- **network** - Emphasize network stats
- **docker** - Emphasize container info
- **minimal** - Compact essential stats only

### Configuration

Create config with `sentinel --init-config`:

```json
{
  "theme": "default",
  "layout": "default",
  "refresh_rate": 2,
  "alerts": {
    "cpu_high": 85,
    "cpu_critical": 95,
    "mem_high": 80,
    "temp_high": 75,
    "battery_low": 20
  },
  "proxy_logs": {
    "nginx": "/var/log/nginx/access.log",
    "caddy": "/var/log/caddy/access.log"
  }
}
```

### Systemd Service

```bash
sudo cp sentinel.service /etc/systemd/system/
sudo systemctl enable --now sentinel
journalctl -u sentinel -f
```

## Requirements

- Python 3.6+
- Linux kernel 4.0+
- Optional: lm-sensors, curl, docker, kubectl

## Changelog

### v0.4.0
- Loading modal with spinner on startup
- Help overlay (press `h`)
- Adjustable refresh rate (`+`/`-` keys, 1-10 seconds)
- Layout modes: default, cpu, network, docker, minimal
- Dynamic Docker/K8s container lists (auto-adjusts to space)
- Improved temperature detection (ARM, VMs, containers)
- Reverse proxy traffic monitoring (nginx/caddy)
- Wider graphs (100 data points)
- Docker volumes with names and sizes
- Performance optimized for low-power devices

### v0.3.0
- Docker container and volume monitoring
- Kubernetes pod/node monitoring  
- Config file support
- 5 color themes
- Alert thresholds
- Systemd service mode
- Per-core CPU bars

### v0.2.0
- btop-inspired UI redesign
- RAPL energy monitoring
- Performance optimization
- Gradient graphs and bars

### v0.1.0
- Initial release

## Open Source

Sentinel is MIT-licensed and built for homelab and Linux users. You can:

- Use it freely on any Linux machine
- Open issues or feature requests on GitHub
- Send pull requests (new panels, themes, bug fixes)
- Fork it and adapt it for your own infrastructure

## License

MIT License - See LICENSE file.
