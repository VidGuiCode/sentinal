# Contributing to Sentinel

Thanks for your interest in contributing to Sentinel! 🛡️

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Your OS and version (e.g., Ubuntu 24.04)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any error messages or logs

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Describe the use case
- Explain why it would be useful
- Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on your system
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Coding Guidelines

- **Python Style**: Follow PEP 8
- **Comments**: Explain why, not what
- **Error Handling**: Fail gracefully, don't crash
- **Performance**: Keep it lightweight (<1% CPU usage)
- **Compatibility**: Test on Ubuntu/Debian at minimum

### Testing

Before submitting:
- [ ] Test on your local system
- [ ] Check for Python errors
- [ ] Verify curses rendering (no flicker)
- [ ] Confirm all features work
- [ ] Test with/without battery
- [ ] Test with/without WireGuard

### Development Setup

```bash
# Clone the repo
git clone https://github.com/VidGuiCode/sentinal.git
cd sentinel

# Make executable
chmod +x sentinel-monitor.py

# Test directly
python3 sentinel-monitor.py

# Or install locally
sudo bash install-sentinel.sh
```

### Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Assume good intentions

## Questions?

Open an issue or start a discussion. We're here to help!

---

Happy coding! 🚀
