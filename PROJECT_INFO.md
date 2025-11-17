# Sentinel Project Information

## 📁 Project Structure

```
sentinel/
├── sentinel-monitor.py       # Main Python application (21KB)
├── install-sentinel.sh        # One-command installer
├── README.md                  # Main documentation
├── LICENSE                    # MIT License
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── GITHUB_SETUP.md            # GitHub publishing guide
├── .gitignore                 # Git ignore rules
└── PROJECT_INFO.md            # This file
```

## 🚀 Quick Start

### Install Locally
```bash
cd /path/to/sentinel
sudo bash install-sentinel.sh
```

### Test Without Installing
```bash
python3 sentinel-monitor.py
```

### Usage
```bash
sentinel    # Full command
sen         # Short alias
```

## 🎯 Project Goals

1. **Universal** - Works on any Linux distribution
2. **Lightweight** - Minimal resource usage (<1% CPU)
3. **Beautiful** - Clean, colorful TUI that doesn't flicker
4. **Informative** - Shows what matters for infrastructure
5. **Smart** - Detects hardware and adapts automatically

## 💡 Key Features

- **CPU Monitoring**: Usage, temp, frequency with warnings
- **Memory Tracking**: Used/available/total
- **Network Intelligence**: Public IP, traffic speed, VPN status
- **Battery/UPS**: Power monitoring for laptops
- **Process Info**: Count and top consumers
- **Real-time**: 2-second cache, smooth updates

## 🛠️ Technologies

- **Language**: Python 3
- **UI**: Curses (terminal interface)
- **Dependencies**: lm-sensors, curl
- **License**: MIT

## 📊 Performance Metrics

- CPU Usage: ~0.5-1%
- Memory: ~15MB
- Update Frequency: 2 seconds (cached)
- Startup Time: <1 second

## 🎨 Design Principles

1. **No Flicker** - Cached data updates
2. **Color Coded** - Green (good), Yellow (warning), Red (critical)
3. **Responsive** - Adapts to terminal size
4. **Fail Gracefully** - Never crashes, logs errors
5. **Universal** - Works on any Linux system

## 📝 Commands Reference

### Keyboard Controls
- `q` - Quit
- `r` - Force refresh (bypass cache)
- `i` - Check public IP immediately

### Installation Locations
- Binary: `/usr/local/bin/sentinel`
- Alias: `/usr/local/bin/sen`
- Bash aliases: `~/.bashrc`

## 🔧 Customization

Current version (v1.0.0) has hardcoded settings. Future versions will support:
- Config file: `~/.config/sentinel/config.yaml`
- Custom themes
- Alert thresholds
- Display toggles

## 🌐 GitHub Repository

Ready to publish! Follow `GITHUB_SETUP.md` for instructions.

Suggested URL: `https://github.com/VidGuiCode/sentinal`

## 📈 Roadmap

### v1.1.0 (Next)
- [ ] Config file support
- [ ] Custom color themes
- [ ] Alert thresholds

### v1.2.0
- [ ] Log export
- [ ] Docker support
- [ ] Prometheus metrics

### v2.0.0
- [ ] Multi-host monitoring
- [ ] Plugin system
- [ ] Web dashboard

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines.

## 📄 License

MIT License - See `LICENSE` file.

## 👤 Author

Created for Open Source Project
Designed to be a universal tool for Linux system monitoring

---

**Sentinel** - Keep watch over your systems 🛡️
