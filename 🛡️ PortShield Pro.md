# 🛡️ PortShield Pro

### Advanced Linux Firewall & Network Security Manager

**PortShield Pro** is a modern, powerful Linux security dashboard built with **Python and PyQt6**. It provides a graphical interface for managing `iptables`, controlling system services, blocking and allowing IP addresses, exporting firewall configurations, and performing network reconnaissance with Nmap.

> **Secure your ports. Control your firewall. Protect your Linux system.**

---

## 🚀 Features

### 🔥 Advanced Firewall Management

Manage Linux `iptables` rules through an intuitive graphical interface.

- ➕ Add TCP/UDP firewall rules
- ✅ ACCEPT traffic
- 🚫 DROP traffic
- ⛔ REJECT traffic
- 🎯 Restrict rules to specific source IPs
- 📋 View current INPUT rules
- 🔄 Refresh firewall state
- 💾 Export firewall configuration
- 💥 Flush INPUT rules with confirmation

---

### 🛡️ IP Security Controls

Quickly manage trusted and unwanted addresses.

**Block an IP**

```text
192.168.1.50
        ↓
      DROP
```

**Allow an IP**

```text
192.168.1.100
        ↓
     ACCEPT
```

PortShield Pro validates IPv4 and IPv6 addresses before executing firewall operations.

---

### 🔍 Network Scanner

Built-in Nmap integration makes basic network reconnaissance available directly from the dashboard.

```bash
nmap -Pn <target>
```

Results are displayed inside the application without requiring a separate terminal.

> ⚠️ Scan only systems you own or have explicit permission to test.

---

### ⚙️ Service Manager

Control common Linux services from the GUI.

| Service | Default Port |
|---|---:|
| SSH | `22` |
| Apache2 | `80` |
| VSFTPD | `21` |
| XRDP | `3389` |

Available actions:

```text
▶ Start
■ Stop
● Status
```

---

### 🔄 Automatic Monitoring

Enable automatic firewall refresh:

```text
☑ Auto Refresh (10s)
```

PortShield Pro periodically reloads the current firewall rules so the dashboard stays synchronized with the system.

---

## 🎨 Modern Security UI

PortShield Pro features a dark, cyber-security inspired interface designed for Linux administrators.

```text
╔══════════════════════════════════════════════╗
║                                              ║
║              P O R T S H I E L D             ║
║                    P R O                     ║
║                                              ║
║        ADVANCED LINUX SECURITY MANAGER       ║
║                                              ║
╚══════════════════════════════════════════════╝
```

### Interface Highlights

- 🌌 Professional dark theme
- 💜 Modern security-focused controls
- 🟢 Status indicators
- 🔴 Destructive-action warnings
- 🔵 Network tools
- 🟠 Backup/export controls
- 📊 Real-time rule display

---

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Application logic |
| 🖼️ PyQt6 | Desktop GUI |
| 🔥 iptables | Linux firewall management |
| 🔎 Nmap | Network scanning |
| ⚙️ systemctl | Service management |
| 🔐 sudo | Privileged operations |

---

## 📋 Requirements

### Operating System

PortShield Pro is designed for **Linux** systems.

### Python

```text
Python 3.9+
PyQt6
```

### System Dependencies

Debian / Ubuntu:

```bash
sudo apt update
sudo apt install iptables nmap
```

The project Python dependency is provided in:

```text
requirements.txt
```

Install it with:

```bash
pip install -r requirements.txt
```

---

## ⚡ Quick Start

Clone the repository:

```bash
git clone https://github.com/yourusername/portshield-pro.git
cd portshield-pro
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python3 portshield.py
```

---

## 🔐 Privileges

PortShield Pro interacts with privileged Linux networking functionality.

Firewall operations use commands such as:

```bash
sudo iptables
sudo iptables-save
```

Service operations use:

```bash
sudo systemctl
```

Make sure your Linux account has appropriate `sudo` privileges.

---

## 💾 Firewall Backup

Before making major firewall changes, export your current configuration:

```bash
sudo iptables-save > firewall_backup.rules
```

PortShield Pro also provides an **Export** button for saving the active firewall configuration.

---

## ⚠️ Security Warning

PortShield Pro can directly modify your system firewall.

Incorrect rules may:

- 🔴 Block SSH access
- 🔴 Disconnect remote administrators
- 🔴 Expose network services
- 🔴 Block legitimate traffic
- 🔴 Disrupt running applications

**Always test firewall changes carefully.**

If you are connected through SSH, make sure you maintain a recovery path before modifying firewall rules.

---

## 🗺️ Roadmap

### PortShield Pro — Future Releases

- [ ] 🧱 nftables support
- [ ] 🌐 Advanced IPv6 support
- [ ] 📊 Traffic monitoring
- [ ] 📈 Network statistics
- [ ] 🔎 Rule search & filtering
- [ ] ✏️ Edit existing rules
- [ ] 🗑️ Delete individual rules
- [ ] 💾 Firewall profiles
- [ ] 📥 Import configurations
- [ ] 📝 Security event logging
- [ ] 🌐 Network interface management
- [ ] 🔔 Security alerts
- [ ] 🌓 Theme customization
- [ ] 📦 AppImage packaging
- [ ] 🐧 Debian package
- [ ] 🚀 Startup service

---

## 📁 Project Structure

```text
portshield-pro/
│
├── portshield.py
├── requirements.txt
├── README.md
│
├── firewall_backup.rules
│
└── assets/
    └── icons/
```

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-security-feature
```

Make your changes, test them on Linux, and submit a pull request.

When contributing, prioritize:

- Security
- Reliability
- Clear error handling
- Safe firewall operations
- Cross-distribution compatibility

---

## ⭐ Why PortShield Pro?

Linux firewall management shouldn't require memorizing every `iptables` command.

PortShield Pro brings essential firewall and network administration tools into one focused desktop application.

```text
        🔥 FIREWALL
             +
        🛡️ SECURITY
             +
        🔍 NETWORK
             +
        ⚙️ SERVICES
             =
       PORTSHIELD PRO
```

---

## 📜 License

Distributed under the license specified in this repository.

See `LICENSE` for details.

---

## 🛡️ PortShield Pro

**Advanced Linux Firewall & Network Security Manager**

> **Secure your ports. Control your system. Defend your network.**

⭐ Star the project if you find it useful.