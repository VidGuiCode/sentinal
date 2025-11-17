# Sentinel - Universal Linux System Monitor 🛡️

A beautiful, lightweight terminal UI (TUI) system monitor for Linux with real-time sparkline graphs and infrastructure-focused monitoring.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

## ✨ Features

### Real-time Monitoring
- **CPU**: Usage, temperature, frequency with warnings (⚠ HIGH, ⚡ SAVING)
- **Memory**: Usage with sparkline history graph
- **Disk**: Multiple mount points with visual bars
- **Network**: Live traffic speed (KB/s) with sparkline graphs for RX/TX
- **Battery**: Level, status, power consumption, health percentage (laptops)
- **Processes**: Total count, top CPU and memory consumers

### Smart Alerts
- CPU frequency warnings (High/Normal/Low)
- Temperature color coding (Green < 60°C, Yellow < 75°C, Red > 80°C)
- Load average alerts based on core count
- Memory pressure indicators
- Battery status icons (⚡ Charging, ⚠ On Battery, ✓ Full)

### Network Intelligence
- Local IP detection
- **Public IP detection** - Shows if exposed to internet
- **WireGuard VPN status** - Auto-detects and shows peer count
- Real-time traffic speed monitoring with history
- Total RX/TX in GB

### Beautiful UI
- **Sparkline graphs** for CPU, Memory, Network (RX/TX)
- Fancy header with double-line borders
- Color-coded progress bars
- Clean section separation
- Temperature visual bars
- Zero flickering (2-second cache)
- Responsive to terminal resize

### Lightweight & Fast
- CPU usage: ~0.5-1%
- Memory footprint: ~15MB
- Smooth 2-second updates
- Non-blocking UI
- Efficient data caching

## 📦 Installation

### Quick Install (Ubuntu/Debian)

```bash
git clone https://github.com/VidGuiCode/sentinal.git
cd sentinel
sudo bash install-sentinel.sh
```

### Manual Installation

```bash
# Install dependencies
sudo apt-get install python3 lm-sensors curl

# Configure sensors
sudo sensors-detect --auto

# Make executable
chmod +x sentinel-monitor.py

# Copy to system path
sudo cp sentinel-monitor.py /usr/local/bin/sentinel
sudo chmod +x /usr/local/bin/sentinel

# Create alias
sudo ln -s /usr/local/bin/sentinel /usr/local/bin/sen
```

## 🚀 Usage

```bash
# Launch Sentinel
sentinel

# Or use short alias
sen
```

### Keyboard Controls

- `q` - Quit
- `r` - Force refresh (bypass 2-second cache)
- `i` - Check public IP immediately

## 📊 What Makes Sentinel Different?

Unlike htop/btop which focus on **process management**, Sentinel is designed for **infrastructure monitoring**:

| Feature | Sentinel | htop | btop |
|---------|----------|------|------|
| **Sparkline graphs** | ✅ | ❌ | ❌ |
| **Public IP detection** | ✅ | ❌ | ❌ |
| **Network traffic speed** | ✅ Live | ❌ | ✅ |
| **VPN status** | ✅ | ❌ | ❌ |
| **Battery health %** | ✅ | ❌ | ✅ |
| **Frequency warnings** | ✅ | ❌ | ❌ |
| **Process tree** | ❌ | ✅ | ✅ |
| **Resource usage** | Low | Low | Medium |

## 🎯 Perfect For

- Home servers & VPS monitoring
- Developer workstations
- Lab environments
- Self-hosted infrastructure
- Raspberry Pi projects
- Any Linux system!

## 🔧 Requirements

- Python 3.6+
- Linux kernel 4.0+
- Terminal with color support
- `lm-sensors` (for temperature monitoring)
- `curl` (for public IP detection)

### Tested On

- Ubuntu 22.04 / 24.04
- Debian 11+
- Raspberry Pi OS
- Arch Linux
- Fedora

## 🎨 Screenshots

```
╔═══════════════════════════════════════════════════════════╗
║                        SENTINEL                           ║
║                  YOUR-HOSTNAME Monitor              22:30 ║
╚═══════════════════════════════════════════════════════════╝

┌─ CPU AMD Ryzen 5 5600U ────────────────────────────────┐
  Usage  ██████░░░░░░░░  15.2%  ▏▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▏
  Temp   47.1°C ▕████░░░░▏  Freq 2.45 GHz  Cores 12
  Load   0.50, 0.45, 0.40  Gov powersave  EPP bal-perf
└─────────────────────────────────────────────────────────┘

┌─ MEMORY ───────────┐  ┌─ STORAGE ──────────┐
  RAM  ████░░░░  42.0%      /     ███░░░░  35.0%
  8420 MB / 15890 MB         175G / 465G
  ▏▂▃▄▅▄▃▂▁▂▃▄▅▄▃▂▁▏        /home 28%
└────────────────────┘  └────────────────────┘

┌─ NETWORK wlp2s0 ───────────────────────────────────────┐
  Local  192.168.1.100    │ Public 203.0.113.45  │ VPN ●
  ↓ Down   45.2 KB/s ▏▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▏
  ↑ Up     12.4 KB/s ▏▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▏
  Total ↓ 125.45 GB  ↑ 23.12 GB    Peers 2 connected
└─────────────────────────────────────────────────────────┘

┌─ BATTERY ⚡ Charging ────────────────────────────────────┐
  Level 100%  ████████████████████  Power 15.2W  Health 95%
└─────────────────────────────────────────────────────────┘

┌─ PROCESSES ─────────────────────────────────────────────┐
  Total 245  │ Top CPU firefox 12.4%  │ Top MEM chrome 8.2%
└─────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────
Uptime 5d 12h 34m          SENTINEL v1.0 - Universal Monitor

⌨ q Quit │ r Refresh │ i IP Check
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

### v1.1.0 (Next)
- [ ] Config file support (`~/.config/sentinel/config.yaml`)
- [ ] Custom color themes
- [ ] Alert thresholds

### v1.2.0
- [ ] Log export
- [ ] Docker container support
- [ ] Prometheus metrics export

### v2.0.0
- [ ] Multi-host monitoring
- [ ] Plugin system
- [ ] Web dashboard

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 🙏 Acknowledgments

Built with Python and curses. Inspired by htop, btop, and the need for infrastructure-focused monitoring.

---

**Sentinel** - Keep watch over your systems 🛡️
