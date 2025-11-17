# Changelog

All notable changes to Sentinel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Configuration file support (`~/.config/sentinel/config.yaml`)
- Custom color themes
- Alert thresholds configuration
- Log export functionality
- Docker container support
- Prometheus metrics export
- Multi-host monitoring
- Plugin system

## [1.0.0] - 2025-11-17

### Added
- Initial release
- Real-time CPU monitoring with usage, temperature, frequency
- CPU frequency status warnings (High/Normal/Low)
- Memory monitoring (used, available, total)
- Disk usage for multiple mount points
- Network monitoring with real-time traffic speed (KB/s)
- Public IP detection
- Local IP display
- WireGuard VPN status detection
- Battery monitoring with UPS mode support
- Power consumption display (watts)
- Process count tracking
- Top CPU and Memory process display
- System uptime tracking
- Color-coded progress bars (Green/Yellow/Red)
- Smart data caching (2-second intervals)
- Keyboard controls (q=quit, r=refresh, i=IP check)
- Beautiful TUI with no flickering
- Automatic hostname detection
- Support for Intel and AMD CPUs
- Graceful error handling

### Technical
- Python 3.6+ support
- Curses-based TUI
- Low resource usage (~0.5-1% CPU, ~15MB RAM)
- Cross-distribution compatibility (Ubuntu, Debian, Arch, etc.)
- Raspberry Pi ARM64 support

### Documentation
- Comprehensive README with installation instructions
- MIT License
- Contributing guidelines
- GitHub setup guide
- One-line installer script

---

## Version Format

- **Major.Minor.Patch** (e.g., 1.0.0)
- **Major**: Breaking changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes, small improvements

[Unreleased]: https://github.com/VidGuiCode/sentinal/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/VidGuiCode/sentinal/releases/tag/v1.0.0
