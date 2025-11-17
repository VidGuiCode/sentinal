# Publishing Sentinel to GitHub

## Step 1: Initialize Git Repository

```bash
cd /path/to/sentinel

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Sentinel v1.0.0 - Universal Linux System Monitor"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `sentinel`
3. Description: "🛡️ A beautiful, real-time terminal UI system monitor for Linux"
4. Choose: Public
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/VidGuiCode/sentinal.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Set Up Repository Settings

### Topics/Tags
Add these topics to help people find your project:
- `linux`
- `system-monitor`
- `tui`
- `terminal`
- `python`
- `monitoring`
- `devops`
- `sysadmin`
- `infrastructure`
- `curses`

### About Section
```
🛡️ A beautiful, real-time terminal UI system monitor for Linux - CPU, Memory, Network, Battery monitoring with smart alerts
```

### Website
Add your demo/docs site if you create one

## Step 5: Add a Screenshot

```bash
# Run Sentinel and take a screenshot
sentinel

# Save as screenshot.png in the repo
# Then commit
git add screenshot.png
git commit -m "Add screenshot"
git push
```

## Step 6: Create First Release

1. Go to Releases → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `Sentinel v1.0.0 - Initial Release`
4. Description:
```markdown
## 🛡️ Sentinel - Universal Linux System Monitor

First stable release of Sentinel!

### Features
- Real-time CPU, Memory, Disk monitoring
- Live network traffic (KB/s)
- Public IP detection
- WireGuard VPN status
- Battery/UPS monitoring
- CPU frequency warnings
- Beautiful color-coded TUI
- Zero flicker, smooth updates

### Installation
```bash
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/sentinel/main/install-sentinel.sh | sudo bash
```

### Requirements
- Python 3.6+
- Linux kernel 4.0+
- lm-sensors, curl

### Tested On
- Ubuntu 22.04 / 24.04
- Debian 11+
- Raspberry Pi OS

---
**Full Changelog**: Initial release
```

5. Upload `sentinel-monitor.py` as an asset
6. Click "Publish release"

## Step 7: Optional - Set Up GitHub Pages

Create a simple landing page:

```bash
# Create docs folder
mkdir docs
cd docs

# Create index.html (basic landing page)
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Sentinel - Linux System Monitor</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 0 20px;
            line-height: 1.6;
        }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        h1 { color: #00a8ff; }
    </style>
</head>
<body>
    <h1>🛡️ Sentinel</h1>
    <p>A beautiful, real-time terminal UI system monitor for Linux</p>

    <h2>Quick Install</h2>
    <pre><code>curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/sentinel/main/install-sentinel.sh | sudo bash</code></pre>

    <h2>Features</h2>
    <ul>
        <li>Real-time CPU, Memory, Disk monitoring</li>
        <li>Live network traffic (KB/s)</li>
        <li>Public IP detection</li>
        <li>Battery/UPS monitoring</li>
        <li>Beautiful color-coded TUI</li>
    </ul>

    <p><a href="https://github.com/VidGuiCode/sentinal">View on GitHub →</a></p>
</body>
</html>
EOF

# Commit
git add docs/
git commit -m "Add GitHub Pages landing page"
git push
```

Then enable GitHub Pages:
1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, /docs folder
4. Save

## Step 8: Promote Your Project

Share on:
- Reddit: r/linux, r/selfhosted, r/homelab
- Hacker News
- Dev.to
- Twitter/X with #Linux #SysAdmin #DevOps

## Maintenance

```bash
# Regular updates
git add .
git commit -m "Description of changes"
git push

# New releases
git tag v1.1.0
git push origin v1.1.0
# Then create release on GitHub
```

---

That's it! Your project is now live on GitHub 🚀
