#!/usr/bin/env python3
"""
Sentinel - Universal Linux System Monitor
A beautiful, real-time TUI dashboard for infrastructure monitoring

GitHub: https://github.com/VidGuiCode/sentinal
License: MIT
"""

import curses
import time
import subprocess
import os
import re
import socket
from datetime import datetime, timedelta
from collections import deque

class SentinelMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.last_update = 0
        self.last_net_bytes = {'rx': 0, 'tx': 0, 'time': time.time()}
        self.cache = {}
        self.hostname = socket.gethostname()

        # History for sparklines (lightweight - only last 20 points)
        self.cpu_history = deque([0] * 20, maxlen=20)
        self.mem_history = deque([0] * 20, maxlen=20)
        self.rx_history = deque([0] * 20, maxlen=20)
        self.tx_history = deque([0] * 20, maxlen=20)

    def run_cmd(self, cmd):
        """Run shell command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2)
            return result.stdout.strip()
        except:
            return ""

    def get_cpu_info(self):
        """Get CPU information"""
        cmd = "top -bn2 -d 0.5 | grep 'Cpu(s)' | tail -1 | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'"
        usage = self.run_cmd(cmd)
        cpu_usage = float(usage) if usage else 0.0
        self.cpu_history.append(cpu_usage)

        temp_output = self.run_cmd("sensors 2>/dev/null | grep -E 'Tctl|Tdie|Core 0|Package id 0' | head -1")
        temp_match = re.search(r'\+(\d+\.\d+)°C', temp_output)
        cpu_temp = float(temp_match.group(1)) if temp_match else 0.0

        freq = self.run_cmd("grep MHz /proc/cpuinfo | awk '{sum+=$4; count++} END {print sum/count}'")
        cpu_freq = float(freq) / 1000 if freq else 0.0

        cpu_model = self.run_cmd("lscpu | grep 'Model name' | sed 's/Model name://g' | sed 's/(R)//g' | sed 's/(TM)//g' | sed 's/CPU//g' | xargs")
        cpu_model = ' '.join(cpu_model.split())[:35]

        cpu_gov = self.run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null") or "N/A"
        cpu_epp = self.run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference 2>/dev/null")
        cpu_epp = cpu_epp.replace("balance_", "bal").replace("_", "-") if cpu_epp else "N/A"

        cores = int(self.run_cmd("nproc") or "0")

        with open('/proc/loadavg', 'r') as f:
            loads = f.read().split()[:3]
            load_avg = [float(x) for x in loads]

        cpu_status = "normal"
        if cpu_freq > 3.5:
            cpu_status = "high"
        elif cpu_freq < 1.5:
            cpu_status = "low"

        return {
            'usage': cpu_usage,
            'temp': cpu_temp,
            'freq': cpu_freq,
            'model': cpu_model,
            'gov': cpu_gov,
            'epp': cpu_epp,
            'cores': cores,
            'load': load_avg,
            'status': cpu_status
        }

    def get_memory_info(self):
        """Get memory usage"""
        output = self.run_cmd("free -m | grep Mem")
        parts = output.split()
        if len(parts) >= 7:
            total = int(parts[1])
            used = int(parts[2])
            available = int(parts[6])
            percent = (used / total) * 100
            self.mem_history.append(percent)
            return {
                'used': used,
                'total': total,
                'available': available,
                'percent': percent
            }
        return {'used': 0, 'total': 0, 'available': 0, 'percent': 0}

    def get_battery_info(self):
        """Get battery information"""
        try:
            capacity = int(self.run_cmd("cat /sys/class/power_supply/BAT0/capacity 2>/dev/null"))
            status = self.run_cmd("cat /sys/class/power_supply/BAT0/status 2>/dev/null")
            power_now = self.run_cmd("cat /sys/class/power_supply/BAT0/power_now 2>/dev/null")
            power_watts = int(power_now) / 1000000 if power_now else 0

            # Health
            full = self.run_cmd("cat /sys/class/power_supply/BAT0/charge_full 2>/dev/null")
            design = self.run_cmd("cat /sys/class/power_supply/BAT0/charge_full_design 2>/dev/null")
            health = (int(full) / int(design)) * 100 if full and design else 0

            return {
                'exists': True,
                'level': capacity,
                'status': status,
                'power': power_watts,
                'health': health
            }
        except:
            return {'exists': False}

    def get_disk_usage(self):
        """Get disk usage"""
        disks = []
        for mount in ['/', '/home']:
            output = self.run_cmd(f"df -h {mount} 2>/dev/null | tail -1")
            parts = output.split()
            if len(parts) >= 5:
                disks.append({
                    'mount': mount,
                    'used': parts[2],
                    'total': parts[1],
                    'percent': int(parts[4].rstrip('%'))
                })
        return disks

    def get_network_info(self):
        """Get network information"""
        default_iface = self.run_cmd("ip route | grep default | awk '{print $5}' | head -1")
        local_ip = self.run_cmd(f"ip -4 addr show {default_iface} 2>/dev/null | grep inet | awk '{{print $2}}' | cut -d/ -f1")
        wg_ip = self.run_cmd("ip addr show wg0 2>/dev/null | grep 'inet ' | awk '{print $2}'")
        wg_active = bool(wg_ip)

        public_ip = "Checking..."
        if hasattr(self, '_public_ip_cache'):
            public_ip = self._public_ip_cache

        current_time = time.time()
        if default_iface:
            rx_bytes = int(self.run_cmd(f"cat /sys/class/net/{default_iface}/statistics/rx_bytes 2>/dev/null || echo 0"))
            tx_bytes = int(self.run_cmd(f"cat /sys/class/net/{default_iface}/statistics/tx_bytes 2>/dev/null || echo 0"))

            time_delta = current_time - self.last_net_bytes['time']
            if time_delta > 0:
                rx_speed = (rx_bytes - self.last_net_bytes['rx']) / time_delta / 1024
                tx_speed = (tx_bytes - self.last_net_bytes['tx']) / time_delta / 1024
            else:
                rx_speed = tx_speed = 0

            self.rx_history.append(rx_speed)
            self.tx_history.append(tx_speed)

            self.last_net_bytes = {
                'rx': rx_bytes,
                'tx': tx_bytes,
                'time': current_time
            }

            rx_total = rx_bytes / (1024**3)
            tx_total = tx_bytes / (1024**3)
        else:
            rx_speed = tx_speed = 0
            rx_total = tx_total = 0

        # WireGuard peer count
        wg_peers = 0
        if wg_active:
            peers_output = self.run_cmd("wg show wg0 peers 2>/dev/null | wc -l")
            wg_peers = int(peers_output) if peers_output else 0

        return {
            'interface': default_iface,
            'local_ip': local_ip,
            'public_ip': public_ip,
            'wg_active': wg_active,
            'wg_ip': wg_ip,
            'wg_peers': wg_peers,
            'rx_speed': rx_speed,
            'tx_speed': tx_speed,
            'rx_total': rx_total,
            'tx_total': tx_total
        }

    def get_public_ip(self):
        """Get public IP"""
        try:
            ip = self.run_cmd("curl -s --max-time 2 ifconfig.me 2>/dev/null || curl -s --max-time 2 icanhazip.com")
            if ip and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                self._public_ip_cache = ip
            else:
                self._public_ip_cache = "N/A"
        except:
            self._public_ip_cache = "N/A"

    def get_processes(self):
        """Get process information"""
        total = int(self.run_cmd("ps aux | wc -l") or "0") - 1
        top_cpu = self.run_cmd("ps aux --sort=-%cpu | head -2 | tail -1 | awk '{print $11\" \"$3\"%\"}'")
        top_mem = self.run_cmd("ps aux --sort=-%mem | head -2 | tail -1 | awk '{print $11\" \"$4\"%\"}'")

        # Shorten names
        if top_cpu and len(top_cpu) > 30:
            parts = top_cpu.rsplit(' ', 1)
            top_cpu = parts[0][:26] + "... " + parts[1] if len(parts) == 2 else top_cpu[:30]
        if top_mem and len(top_mem) > 30:
            parts = top_mem.rsplit(' ', 1)
            top_mem = parts[0][:26] + "... " + parts[1] if len(parts) == 2 else top_mem[:30]

        return {
            'total': total,
            'top_cpu': top_cpu,
            'top_mem': top_mem
        }

    def get_uptime(self):
        """Calculate system uptime"""
        uptime_seconds = float(self.run_cmd("cat /proc/uptime | awk '{print $1}'"))
        uptime = timedelta(seconds=int(uptime_seconds))
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        return days, hours, minutes

    def draw_sparkline(self, stdscr, y, x, width, data, max_val=100):
        """Draw a mini sparkline graph - lightweight!"""
        if not data or width <= 0:
            return

        bars = "▁▂▃▄▅▆▇█"
        points = list(data)[-width:]

        try:
            for i, value in enumerate(points):
                if i >= width:
                    break
                normalized = min(value / max_val, 1.0) if max_val > 0 else 0
                bar_index = int(normalized * (len(bars) - 1))

                if normalized < 0.5:
                    color = curses.color_pair(2)
                elif normalized < 0.8:
                    color = curses.color_pair(3)
                else:
                    color = curses.color_pair(4)

                stdscr.addstr(y, x + i, bars[bar_index], color)
        except:
            pass

    def draw_header(self, stdscr, width):
        """Draw beautiful header"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        try:
            # Fancy border
            stdscr.addstr(0, 0, "╔" + "═" * (width - 2) + "╗", curses.color_pair(1) | curses.A_BOLD)

            # Title
            title = "SENTINEL"
            title_x = (width - len(title)) // 2
            stdscr.addstr(1, 0, "║", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(1, title_x, title, curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(1, width - 1, "║", curses.color_pair(1) | curses.A_BOLD)

            # Subtitle
            subtitle = f"{self.hostname.upper()} Monitor"
            subtitle_x = (width - len(subtitle)) // 2
            stdscr.addstr(2, 0, "║", curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(2, subtitle_x, subtitle, curses.color_pair(6))
            stdscr.addstr(2, width - len(timestamp) - 3, timestamp, curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(2, width - 1, "║", curses.color_pair(1) | curses.A_BOLD)

            stdscr.addstr(3, 0, "╚" + "═" * (width - 2) + "╝", curses.color_pair(1) | curses.A_BOLD)
        except:
            pass

    def draw_bar(self, stdscr, y, x, width, percent, show_percent=True):
        """Draw progress bar"""
        filled = int((width * percent) / 100)

        if percent < 50:
            color = curses.color_pair(2)
        elif percent < 80:
            color = curses.color_pair(3)
        else:
            color = curses.color_pair(4)

        try:
            if filled > 0:
                stdscr.addstr(y, x, "█" * filled, color | curses.A_BOLD)
            if filled < width:
                stdscr.addstr(y, x + filled, "░" * (width - filled), curses.color_pair(8))
            if show_percent:
                pct_str = f"{percent:5.1f}%"
                stdscr.addstr(y, x + width + 2, pct_str, color | curses.A_BOLD)
        except:
            pass

    def update_data(self):
        """Update all system data"""
        current_time = time.time()

        if current_time - self.last_update < 2:
            return self.cache

        if not hasattr(self, '_last_ip_check') or current_time - self._last_ip_check > 30:
            self.get_public_ip()
            self._last_ip_check = current_time

        self.cache = {
            'cpu': self.get_cpu_info(),
            'mem': self.get_memory_info(),
            'battery': self.get_battery_info(),
            'disk': self.get_disk_usage(),
            'network': self.get_network_info(),
            'processes': self.get_processes(),
            'uptime': self.get_uptime(),
        }

        self.last_update = current_time
        return self.cache

    def draw(self, stdscr):
        """Main draw function"""
        curses.curs_set(0)
        stdscr.timeout(500)

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_RED, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)
        curses.init_pair(8, 240, -1)

        while True:
            try:
                height, width = stdscr.getmaxyx()
                stdscr.erase()

                data = self.update_data()
                self.draw_header(stdscr, width)

                row = 5

                # ═══ CPU ═══
                cpu = data['cpu']
                stdscr.addstr(row, 2, "┌─ CPU ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(cpu['model'], curses.color_pair(6))
                stdscr.addstr(" " + "─" * max(1, width - len(cpu['model']) - 11) + "┐", curses.color_pair(1))
                row += 1

                stdscr.addstr(row, 4, "Usage ", curses.color_pair(7))
                self.draw_bar(stdscr, row, 10, 40, cpu['usage'])
                stdscr.addstr(row, 60, "▏", curses.color_pair(8))
                self.draw_sparkline(stdscr, row, 61, 20, self.cpu_history)
                stdscr.addstr(row, 81, "▕", curses.color_pair(8))
                row += 1

                # Temp with visual bar
                temp_color = curses.color_pair(2) if cpu['temp'] < 60 else curses.color_pair(3) if cpu['temp'] < 75 else curses.color_pair(4)
                stdscr.addstr(row, 4, "Temp  ", curses.color_pair(7))
                stdscr.addstr(f"{cpu['temp']:5.1f}°C", temp_color | curses.A_BOLD)

                temp_bar_width = 12
                temp_percent = min((cpu['temp'] / 100) * 100, 100)
                temp_filled = int((temp_bar_width * temp_percent) / 100)
                stdscr.addstr(row, 22, "▕", curses.color_pair(8))
                if temp_filled > 0:
                    stdscr.addstr("█" * temp_filled, temp_color)
                if temp_filled < temp_bar_width:
                    stdscr.addstr("░" * (temp_bar_width - temp_filled), curses.color_pair(8))
                stdscr.addstr("▏", curses.color_pair(8))

                # Frequency
                freq_color = curses.color_pair(2)
                freq_status = ""
                if cpu['status'] == 'high':
                    freq_color = curses.color_pair(4)
                    freq_status = " ⚠"
                elif cpu['status'] == 'low':
                    freq_color = curses.color_pair(3)
                    freq_status = " ⚡"

                stdscr.addstr(row, 40, "Freq ", curses.color_pair(7))
                stdscr.addstr(f"{cpu['freq']:.2f} GHz", freq_color | curses.A_BOLD)
                if freq_status:
                    stdscr.addstr(freq_status, freq_color | curses.A_BOLD)

                stdscr.addstr(row, 64, f"Cores {cpu['cores']}", curses.color_pair(6))
                row += 1

                # Load
                stdscr.addstr(row, 4, "Load  ", curses.color_pair(7))
                for i, load in enumerate(cpu['load']):
                    load_color = curses.color_pair(2) if load < cpu['cores'] * 0.7 else curses.color_pair(3) if load < cpu['cores'] else curses.color_pair(4)
                    stdscr.addstr(f"{load:.2f}", load_color | curses.A_BOLD)
                    if i < 2:
                        stdscr.addstr(", ", curses.color_pair(8))

                stdscr.addstr(row, 30, f"Gov {cpu['gov']}", curses.color_pair(8))
                stdscr.addstr(row, 48, f"EPP {cpu['epp']}", curses.color_pair(8))
                row += 1

                stdscr.addstr(row, 2, "└" + "─" * (width - 4) + "┘", curses.color_pair(1))
                row += 2

                # ═══ MEMORY & DISK ═══
                col_width = (width - 6) // 2
                mem = data['mem']

                stdscr.addstr(row, 2, "┌─ MEMORY ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr("─" * (col_width - 12) + "┐", curses.color_pair(1))

                stdscr.addstr(row, col_width + 2, "┌─ STORAGE ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr("─" * (col_width - 13) + "┐", curses.color_pair(1))
                row += 1

                # Memory
                stdscr.addstr(row, 4, "RAM ", curses.color_pair(7))
                self.draw_bar(stdscr, row, 8, col_width - 22, mem['percent'])
                row += 1
                stdscr.addstr(row, 4, f"{mem['used']} MB / {mem['total']} MB", curses.color_pair(8))
                stdscr.addstr(row, col_width - 18, f"Free {mem['available']} MB", curses.color_pair(6))
                row += 1
                stdscr.addstr(row, 4, "▏", curses.color_pair(8))
                self.draw_sparkline(stdscr, row, 5, col_width - 7, self.mem_history)
                stdscr.addstr(row, col_width - 2, "▕", curses.color_pair(8))

                # Disk
                disks = data['disk']
                disk_row = row - 2
                for i, disk in enumerate(disks[:2]):
                    if i == 0:
                        stdscr.addstr(disk_row, col_width + 4, f"{disk['mount']:5s}", curses.color_pair(7))
                        self.draw_bar(stdscr, disk_row, col_width + 10, col_width - 24, disk['percent'])
                        disk_row += 1
                        stdscr.addstr(disk_row, col_width + 4, f"{disk['used']} / {disk['total']}", curses.color_pair(8))
                    else:
                        disk_row += 1
                        stdscr.addstr(disk_row, col_width + 4, f"{disk['mount']:5s} {disk['percent']}%", curses.color_pair(8))

                row += 1
                stdscr.addstr(row, 2, "└" + "─" * (col_width - 2) + "┘", curses.color_pair(1))
                stdscr.addstr(row, col_width + 2, "└" + "─" * (col_width - 2) + "┘", curses.color_pair(1))
                row += 2

                # ═══ NETWORK ═══
                net = data['network']
                stdscr.addstr(row, 2, "┌─ NETWORK ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(f"{net['interface']} ", curses.color_pair(6))
                stdscr.addstr("─" * (width - 15 - len(net['interface'])) + "┐", curses.color_pair(1))
                row += 1

                stdscr.addstr(row, 4, "Local ", curses.color_pair(7))
                stdscr.addstr(f"{net['local_ip']:15s}", curses.color_pair(6) | curses.A_BOLD)
                stdscr.addstr(row, 30, "│ Public ", curses.color_pair(7))
                public_color = curses.color_pair(4) if net['public_ip'] not in ["N/A", "Checking..."] else curses.color_pair(8)
                stdscr.addstr(f"{net['public_ip']:15s}", public_color | curses.A_BOLD)

                if net['wg_active']:
                    stdscr.addstr(row, 60, "│ VPN ", curses.color_pair(7))
                    stdscr.addstr("●", curses.color_pair(2) | curses.A_BOLD)
                row += 1

                # Traffic with sparklines
                stdscr.addstr(row, 4, "↓ Down", curses.color_pair(2))
                stdscr.addstr(f" {net['rx_speed']:7.1f} KB/s", curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(row, 30, "▏", curses.color_pair(8))
                max_rx = max(self.rx_history) if max(self.rx_history) > 0 else 100
                self.draw_sparkline(stdscr, row, 31, 15, self.rx_history, max_val=max_rx)
                stdscr.addstr(row, 46, "▕", curses.color_pair(8))

                stdscr.addstr(row, 50, "↑ Up", curses.color_pair(6))
                stdscr.addstr(f" {net['tx_speed']:7.1f} KB/s", curses.color_pair(6) | curses.A_BOLD)
                stdscr.addstr(row, 70, "▏", curses.color_pair(8))
                max_tx = max(self.tx_history) if max(self.tx_history) > 0 else 100
                self.draw_sparkline(stdscr, row, 71, 14, self.tx_history, max_val=max_tx)
                stdscr.addstr(row, 85, "▕", curses.color_pair(8))
                row += 1

                stdscr.addstr(row, 4, f"Total ↓ {net['rx_total']:.2f} GB  ↑ {net['tx_total']:.2f} GB", curses.color_pair(8))

                if net['wg_active']:
                    stdscr.addstr(row, 50, "Peers ", curses.color_pair(7))
                    peer_str = f"{net['wg_peers']} connected"
                    stdscr.addstr(peer_str, curses.color_pair(6) | curses.A_BOLD)
                row += 1

                stdscr.addstr(row, 2, "└" + "─" * (width - 4) + "┘", curses.color_pair(1))
                row += 2

                # ═══ BATTERY ═══
                battery = data['battery']
                if battery['exists']:
                    stdscr.addstr(row, 2, "┌─ BATTERY ", curses.color_pair(1) | curses.A_BOLD)

                    if battery['status'] == "Charging":
                        stdscr.addstr("⚡ Charging ", curses.color_pair(3) | curses.A_BOLD)
                    elif battery['status'] == "Discharging":
                        stdscr.addstr("⚠ On Battery ", curses.color_pair(4) | curses.A_BOLD)
                    else:
                        stdscr.addstr("✓ Full ", curses.color_pair(2) | curses.A_BOLD)

                    stdscr.addstr("─" * (width - 28) + "┐", curses.color_pair(1))
                    row += 1

                    battery_color = curses.color_pair(2) if battery['level'] > 50 else curses.color_pair(3) if battery['level'] > 20 else curses.color_pair(4)
                    stdscr.addstr(row, 4, "Level ", curses.color_pair(7))
                    stdscr.addstr(f"{battery['level']:3d}%", battery_color | curses.A_BOLD)

                    self.draw_bar(stdscr, row, 15, 30, battery['level'], show_percent=False)

                    if battery['power'] > 0:
                        stdscr.addstr(row, 50, f"Power {battery['power']:.1f}W", curses.color_pair(6))

                    if battery['health'] > 0:
                        health_color = curses.color_pair(2) if battery['health'] > 80 else curses.color_pair(3)
                        stdscr.addstr(row, 66, f"Health {battery['health']:.0f}%", health_color)
                    row += 1

                    stdscr.addstr(row, 2, "└" + "─" * (width - 4) + "┘", curses.color_pair(1))
                    row += 2

                # ═══ PROCESSES ═══
                proc = data['processes']
                stdscr.addstr(row, 2, "┌─ PROCESSES ", curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr("─" * (width - 16) + "┐", curses.color_pair(1))
                row += 1

                stdscr.addstr(row, 4, "Total ", curses.color_pair(7))
                stdscr.addstr(f"{proc['total']}", curses.color_pair(6) | curses.A_BOLD)

                if proc['top_cpu']:
                    stdscr.addstr(row, 16, "│ Top CPU ", curses.color_pair(7))
                    stdscr.addstr(f"{proc['top_cpu']}", curses.color_pair(3))

                if proc['top_mem']:
                    stdscr.addstr(row, 52, "│ Top MEM ", curses.color_pair(7))
                    stdscr.addstr(f"{proc['top_mem']}", curses.color_pair(3))
                row += 1

                stdscr.addstr(row, 2, "└" + "─" * (width - 4) + "┘", curses.color_pair(1))
                row += 2

                # ═══ FOOTER ═══
                days, hours, minutes = data['uptime']
                stdscr.addstr(row, 2, "─" * (width - 4), curses.color_pair(5))
                row += 1

                stdscr.addstr(row, 4, "Uptime ", curses.color_pair(7))
                stdscr.addstr(f"{days}d {hours}h {minutes}m", curses.color_pair(2) | curses.A_BOLD)

                stdscr.addstr(row, width - 42, "SENTINEL v1.0 - Universal Monitor", curses.color_pair(1))

                # Controls
                stdscr.addstr(height - 1, 2, "⌨ ", curses.color_pair(6))
                stdscr.addstr("q", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(" Quit │ ", curses.color_pair(8))
                stdscr.addstr("r", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(" Refresh │ ", curses.color_pair(8))
                stdscr.addstr("i", curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(" IP Check", curses.color_pair(8))

                stdscr.refresh()

                # Input
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('r') or key == ord('R'):
                    self.last_update = 0
                    continue
                elif key == ord('i') or key == ord('I'):
                    self._last_ip_check = 0
                    continue

            except curses.error:
                pass
            except Exception as e:
                with open('/tmp/sentinel.log', 'a') as f:
                    f.write(f"{datetime.now()}: {e}\n")

def main():
    try:
        monitor = SentinelMonitor()
        curses.wrapper(monitor.draw)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
