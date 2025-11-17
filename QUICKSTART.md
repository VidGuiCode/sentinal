# Sentinel - Quick Start Guide

## Installation (30 seconds)

```bash
cd /path/to/sentinel
sudo bash install-sentinel.sh
```

Done! ✅

## Usage

```bash
sentinel    # Launch monitor
sen         # Short version
```

## What You'll See

```
═══ SENTINEL MONITOR - YOUR-HOSTNAME ═══              22:30:45

┌─ CPU AMD Ryzen 5 5600U ──────────────────────────────────┐
  Usage:      ██████░░░░░░░░░░░░░░░░░░░░░░░░  15.2%

  Temp: 47.1°C  │ Freq: 2.45 GHz  │ Cores: 12
  Gov: powersave │ EPP: bal_performance │ Load: 0.50, 0.45, 0.40
└──────────────────────────────────────────────────────────┘

┌─ MEMORY ──────────┐  ┌─ STORAGE ─────────┐
  RAM: ████░░░░  42%      Root: ███░░░░  35%
  8420 MB / 15890 MB      175G / 465G
└───────────────────┘  └───────────────────┘

┌─ NETWORK wlp2s0 ──────────────────────────────────────────┐
  Local IP:  192.168.1.100  │ Public IP: 203.0.113.45
  Traffic:   ↓    45.2 KB/s  ↑    12.4 KB/s
  │ Total: ↓ 125.45 GB  ↑ 23.12 GB
└──────────────────────────────────────────────────────────┘

┌─ BATTERY UPS Mode ────────────────────────────────────────┐
  Level: 100%  ████████████████████  │ Status: Full
└──────────────────────────────────────────────────────────┘

┌─ PROCESSES ───────────────────────────────────────────────┐
  Total: 245  │ Top CPU: firefox 12.4%  │ Top MEM: chrome 8.2%
└──────────────────────────────────────────────────────────┘

──────────────────────────────────────────────────────────
Uptime: 5d 12h 34m          Sentinel v1.0 - Universal Monitor

Press 'q' to quit  │  'r' to refresh  │  'i' for IP check
```

## Key Features

### 🎯 CPU Monitoring
- **Usage**: Real-time percentage
- **Temperature**: Color-coded (Green/Yellow/Red)
- **Frequency**: With warnings (⚠ HIGH, ⚡ SAVING)
- **Load Average**: 1m, 5m, 15m

### 💾 Memory & Storage
- **RAM**: Used/Total/Available
- **Disk**: Multiple mount points
- **Visual bars**: Easy to scan

### 🌐 Network
- **Local IP**: Your LAN address
- **Public IP**: Internet-facing IP (warns if exposed)
- **Live Traffic**: KB/s down/up speed
- **WireGuard**: Auto-detects VPN

### 🔋 Battery (Laptops)
- **Level**: Percentage
- **Status**: Charging/Discharging/Full
- **Power**: Watts consumption
- **UPS Mode**: Automatic failover

### ⚙️ Process Info
- **Total**: Process count
- **Top CPU**: Highest CPU user
- **Top MEM**: Highest memory user

## Keyboard Controls

| Key | Action |
|-----|--------|
| `q` | Quit Sentinel |
| `r` | Force refresh (bypass 2-sec cache) |
| `i` | Check public IP immediately |

## Color Guide

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Good (< 50%) |
| 🟡 **Yellow** | Warning (50-80%) |
| 🔴 **Red** | Critical (> 80%) |
| 🔵 **Blue** | Borders/UI |
| 🟣 **Magenta** | Accents |
| ⚪ **White** | Normal text |

## CPU Frequency Warnings

- **⚠ HIGH** (>3.5 GHz) - Running hot, performance mode
- **Normal** (1.5-3.5 GHz) - Balanced operation
- **⚡ SAVING** (<1.5 GHz) - Power saving mode

## Tips

1. **Terminal Size**: Works best at 100x30 or larger
2. **Updates**: Data refreshes every 2 seconds (efficient)
3. **Public IP**: Checks every 30 seconds (not every refresh)
4. **No Sudo**: Run as normal user, no root needed
5. **Exit**: Press `q` anytime to quit

## Troubleshooting

### No temperature shown?
```bash
sudo sensors-detect --auto
```

### Public IP shows "N/A"?
```bash
# Press 'i' to force check
# Or check internet: ping 8.8.8.8
```

### Permission denied?
```bash
sudo chmod +x /usr/local/bin/sentinel
```

## Uninstall

```bash
sudo rm /usr/local/bin/sentinel
sudo rm /usr/local/bin/sen
# Remove aliases from ~/.bashrc manually
```

## Learn More

- **README.md** - Full documentation
- **CONTRIBUTING.md** - How to contribute
- **CHANGELOG.md** - Version history

---

**Enjoy monitoring!** 🛡️
