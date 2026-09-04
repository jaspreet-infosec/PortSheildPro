import sys
import subprocess
import ipaddress

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox,
    QTabWidget, QGridLayout, QGroupBox, QCheckBox, QFrame,
    QSizePolicy, QSplitter,
)

from PyQt6.QtCore import Qt, QTimer

# =========================================================
# VALIDATION
# =========================================================

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_port(port):
    return port.isdigit() and 0 < int(port) <= 65535


# =========================================================
# STYLESHEET
# =========================================================

STYLE = """

QWidget {
    background-color: #0d0d1a;
    color: #cdc8e8;
    font-family: Segoe UI;
    font-size: 13px;
}

/* TABS */

QTabWidget::pane {
    border: 1px solid #2a2a5a;
    background: #0f0f22;
}

QTabBar::tab {
    background: #11112a;
    color: #6666aa;
    padding: 12px 28px;
    border: 1px solid #2a2a5a;
    border-bottom: none;
    min-width: 140px;
    font-weight: bold;
}

QTabBar::tab:selected {
    color: #bd93f9;
    border-color: #bd93f9;
}

/* GROUP BOX */

QGroupBox {
    background: #11112a;
    border: 1px solid #2a2a5a;
    border-radius: 12px;
    margin-top: 18px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 10px;
    color: #bd93f9;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 3px;
}

/* INPUTS */

QLineEdit,
QComboBox {
    background: #09091e;
    border: 1px solid #2a2a5a;
    border-radius: 8px;
    padding: 10px 12px;
    color: #f8f8f2;
    min-height: 22px;
}

QLineEdit:focus,
QComboBox:focus {
    border: 1px solid #bd93f9;
}

/* TEXT AREA */

QTextEdit {
    background: #07071a;
    border: 1px solid #1e1e44;
    border-radius: 10px;
    padding: 12px;
    color: #50fa7b;
    font-family: Consolas;
}

/* BUTTON */

QPushButton {
    background: #13132e;
    color: #aaaaee;
    border: 1px solid #2a2a5a;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 12px;
    font-weight: bold;
    min-height: 44px;
}

QPushButton:hover {
    background: #1c1c40;
    border-color: #5050aa;
}

QPushButton#primary {
    background: #2b1258;
    border: 1px solid #6a35c8;
    color: #d5b3ff;
}

QPushButton#danger {
    background: #2a0818;
    border: 1px solid #8a2060;
    color: #ff79c6;
}

QPushButton#success {
    background: #082018;
    border: 1px solid #207840;
    color: #50fa7b;
}

QPushButton#warn {
    background: #2a1808;
    border: 1px solid #885520;
    color: #ffb86c;
}

QPushButton#info {
    background: #082030;
    border: 1px solid #206888;
    color: #8be9fd;
}

/* CHECKBOX */

QCheckBox {
    color: #8888cc;
    font-size: 11px;
    font-weight: bold;
}

/* SCROLLBAR */

QScrollBar:vertical {
    background: #07071a;
    width: 6px;
}

QScrollBar::handle:vertical {
    background: #2a2a5a;
    border-radius: 3px;
}

"""


# =========================================================
# MAIN GUI
# =========================================================

class PortShieldGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "PortShield - Advanced Linux Firewall Manager"
        )

        self.resize(1400, 900)

        self.showMaximized()

        self.setStyleSheet(STYLE)

        root = QVBoxLayout(self)

        root.setContentsMargins(18, 14, 18, 12)

        root.setSpacing(12)

        # =====================================================
        # HEADER
        # =====================================================

        header = QLabel("PORTSHIELD")

        header.setStyleSheet("""
            font-size: 28px;
            font-weight: 900;
            letter-spacing: 6px;
            color: #8be9fd;
        """)

        sub = QLabel(
            "ADVANCED LINUX FIREWALL MANAGER"
        )

        sub.setStyleSheet("""
            color: #444488;
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 5px;
        """)

        top = QVBoxLayout()

        top.addWidget(header)

        top.addWidget(sub)

        root.addLayout(top)

        # =====================================================
        # TABS
        # =====================================================

        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.create_firewall_tab(),
            "🔒 Firewall"
        )

        self.tabs.addTab(
            self.create_services_tab(),
            "⚙ Services"
        )

        root.addWidget(self.tabs)

        # =====================================================
        # FOOTER
        # =====================================================

        footer = QHBoxLayout()

        self.auto_refresh = QCheckBox(
            "Auto Refresh (10s)"
        )

        self.auto_refresh.stateChanged.connect(
            self.toggle_auto_refresh
        )

        self.status = QLabel("Firewall Active")

        self.status.setStyleSheet("""
            color: #50fa7b;
            font-weight: bold;
        """)

        footer.addWidget(self.auto_refresh)

        footer.addStretch()

        footer.addWidget(self.status)

        root.addLayout(footer)

        self.timer = QTimer()

        self.timer.timeout.connect(self.load_rules)

    # =========================================================
    # AUTO REFRESH
    # =========================================================

    def toggle_auto_refresh(self, state):

        if state == Qt.CheckState.Checked.value:
            self.timer.start(10000)
        else:
            self.timer.stop()

    # =========================================================
    # FIREWALL TAB
    # =========================================================

    def create_firewall_tab(self):

        tab = QWidget()

        outer = QVBoxLayout(tab)

        outer.setSpacing(12)

        # =====================================================
        # SPLITTER
        # =====================================================

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setMinimumHeight(320)

        # =====================================================
        # LEFT CARD
        # =====================================================

        rule_card = QGroupBox(
            "CREATE FIREWALL RULE"
        )

        rg = QGridLayout(rule_card)

        rg.setSpacing(10)

        rg.setContentsMargins(
            14,
            24,
            14,
            14
        )

        rg.addWidget(QLabel("Protocol"), 0, 0)

        self.proto_box = QComboBox()

        self.proto_box.addItems([
            "tcp",
            "udp"
        ])

        rg.addWidget(self.proto_box, 0, 1)

        rg.addWidget(QLabel("Port"), 1, 0)

        self.port_input = QLineEdit()

        self.port_input.setPlaceholderText(
            "22, 80, 443"
        )

        rg.addWidget(self.port_input, 1, 1)

        rg.addWidget(QLabel("Action"), 2, 0)

        self.action_box = QComboBox()

        self.action_box.addItems([
            "ACCEPT",
            "DROP",
            "REJECT"
        ])

        rg.addWidget(self.action_box, 2, 1)

        rg.addWidget(QLabel("Source IP"), 3, 0)

        self.ip_filter_input = QLineEdit()

        self.ip_filter_input.setPlaceholderText(
            "Optional"
        )

        rg.addWidget(
            self.ip_filter_input,
            3,
            1
        )

        self.add_btn = QPushButton(
            "⊕ ADD RULE"
        )

        self.add_btn.setObjectName("primary")

        self.add_btn.clicked.connect(
            self.add_rule
        )

        rg.addWidget(
            self.add_btn,
            4,
            0,
            1,
            2
        )

        splitter.addWidget(rule_card)

        # =====================================================
        # RIGHT PANEL
        # =====================================================

        right_widget = QWidget()

        rv = QVBoxLayout(right_widget)

        rv.setSpacing(10)

        # =====================================================
        # BLOCK / UNBLOCK
        # =====================================================

        block_card = QGroupBox(
            "BLOCK / UNBLOCK IP"
        )

        bl = QHBoxLayout(block_card)

        bl.setSpacing(10)

        bl.setContentsMargins(
            14,
            24,
            14,
            14
        )

        self.block_ip_input = QLineEdit()

        self.block_ip_input.setPlaceholderText(
            "xxx.xxx.xxx.xxx"
        )

        block_btn = QPushButton(
            "🚫 Block"
        )

        block_btn.setObjectName(
            "danger"
        )

        block_btn.setMinimumWidth(130)

        block_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        unblock_btn = QPushButton(
            "✔ Unblock"
        )

        unblock_btn.setObjectName(
            "success"
        )

        unblock_btn.setMinimumWidth(130)

        unblock_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        block_btn.clicked.connect(
            self.block_ip
        )

        unblock_btn.clicked.connect(
            self.unblock_ip
        )

        bl.addWidget(self.block_ip_input)

        bl.addWidget(block_btn)

        bl.addWidget(unblock_btn)

        rv.addWidget(block_card)

        # =====================================================
        # ALLOW IP
        # =====================================================

        allow_card = QGroupBox(
            "ALLOW SPECIFIC IP"
        )

        al = QHBoxLayout(allow_card)

        al.setSpacing(10)

        al.setContentsMargins(
            14,
            24,
            14,
            14
        )

        self.allow_ip_input = QLineEdit()

        self.allow_ip_input.setPlaceholderText(
            "xxx.xxx.xxx.xxx"
        )

        allow_btn = QPushButton(
            "✅ Allow IP"
        )

        allow_btn.setObjectName(
            "success"
        )

        allow_btn.setMinimumWidth(150)

        allow_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        allow_btn.clicked.connect(
            self.allow_ip
        )

        al.addWidget(self.allow_ip_input)

        al.addWidget(allow_btn)

        rv.addWidget(allow_card)

        # =====================================================
        # CONTROLS
        # =====================================================

        ctrl_card = QGroupBox(
            "FIREWALL CONTROLS"
        )

        cl = QHBoxLayout(ctrl_card)

        cl.setSpacing(10)

        cl.setContentsMargins(
            14,
            24,
            14,
            14
        )

        refresh_btn = QPushButton(
            "🔄 Refresh"
        )

        flush_btn = QPushButton(
            "💥 Flush Rules"
        )

        export_btn = QPushButton(
            "💾 Export"
        )

        flush_btn.setObjectName(
            "danger"
        )

        export_btn.setObjectName(
            "warn"
        )

        refresh_btn.clicked.connect(
            self.load_rules
        )

        flush_btn.clicked.connect(
            self.flush_rules
        )

        export_btn.clicked.connect(
            self.export_rules
        )

        for b in (
            refresh_btn,
            flush_btn,
            export_btn
        ):

            b.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )

        cl.addWidget(refresh_btn)

        cl.addWidget(flush_btn)

        cl.addWidget(export_btn)

        rv.addWidget(ctrl_card)

        rv.addStretch()

        splitter.addWidget(right_widget)

        splitter.setStretchFactor(0, 2)

        splitter.setStretchFactor(1, 3)

        outer.addWidget(splitter)

        # =====================================================
        # RULE DISPLAY
        # =====================================================

        rules_card = QGroupBox(
            "CURRENT IPTABLES RULES"
        )

        rules_layout = QVBoxLayout(
            rules_card
        )

        rules_layout.setContentsMargins(
            12,
            24,
            12,
            12
        )

        self.rules_display = QTextEdit()

        self.rules_display.setReadOnly(True)

        rules_layout.addWidget(
            self.rules_display
        )

        outer.addWidget(
            rules_card,
            stretch=2
        )

        # =====================================================
        # NMAP
        # =====================================================

        scan_card = QGroupBox(
            "PORT SCAN — NMAP"
        )

        scan_layout = QVBoxLayout(
            scan_card
        )

        scan_layout.setSpacing(10)

        scan_layout.setContentsMargins(
            12,
            24,
            12,
            12
        )

        scan_row = QHBoxLayout()

        self.nmap_ip_input = QLineEdit()

        self.nmap_ip_input.setPlaceholderText(
            "Target IP"
        )

        scan_btn = QPushButton(
            "🔍 Scan Target"
        )

        scan_btn.setObjectName("info")

        scan_btn.setMinimumWidth(180)

        scan_btn.clicked.connect(
            self.run_nmap
        )

        scan_row.addWidget(
            self.nmap_ip_input
        )

        scan_row.addWidget(scan_btn)

        scan_layout.addLayout(scan_row)

        self.nmap_result = QTextEdit()

        self.nmap_result.setReadOnly(True)

        scan_layout.addWidget(
            self.nmap_result
        )

        outer.addWidget(
            scan_card,
            stretch=2
        )

        self.load_rules()

        return tab

    # =========================================================
    # SERVICES TAB
    # =========================================================

    def create_services_tab(self):

        tab = QWidget()

        layout = QVBoxLayout(tab)

        title = QLabel(
            "SYSTEM SERVICE MANAGER"
        )

        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 5px;
            color: #bd93f9;
        """)

        layout.addWidget(title)

        self.services = {
            "ssh": "22",
            "apache2": "80",
            "vsftpd": "21",
            "xrdp": "3389"
        }

        self.status_labels = {}

        box = QGroupBox(
            "MANAGED SERVICES"
        )

        grid = QGridLayout(box)

        headers = [
            "Service",
            "Port",
            "Start",
            "Stop",
            "Status"
        ]

        for i, h in enumerate(headers):

            lbl = QLabel(h)

            lbl.setStyleSheet("""
                color: #6666aa;
                font-weight: bold;
            """)

            grid.addWidget(lbl, 0, i)

        for row, (
            service,
            port
        ) in enumerate(
            self.services.items(),
            start=1
        ):

            grid.addWidget(
                QLabel(service.upper()),
                row,
                0
            )

            grid.addWidget(
                QLabel(f":{port}"),
                row,
                1
            )

            start_btn = QPushButton(
                "▶ Start"
            )

            stop_btn = QPushButton(
                "■ Stop"
            )

            start_btn.setObjectName(
                "success"
            )

            stop_btn.setObjectName(
                "danger"
            )

            start_btn.clicked.connect(
                lambda _, s=service:
                self.toggle_service(
                    s,
                    "start"
                )
            )

            stop_btn.clicked.connect(
                lambda _, s=service:
                self.toggle_service(
                    s,
                    "stop"
                )
            )

            grid.addWidget(
                start_btn,
                row,
                2
            )

            grid.addWidget(
                stop_btn,
                row,
                3
            )

            status_lbl = QLabel(
                "checking..."
            )

            self.status_labels[
                service
            ] = status_lbl

            grid.addWidget(
                status_lbl,
                row,
                4
            )

            self.update_service_status(
                service
            )

        layout.addWidget(box)

        layout.addStretch()

        return tab

    # =========================================================
    # SERVICE CONTROL
    # =========================================================

    def toggle_service(
        self,
        service,
        action
    ):

        subprocess.run(
            [
                "sudo",
                "systemctl",
                action,
                service
            ],
            capture_output=True
        )

        self.update_service_status(
            service
        )

    def update_service_status(
        self,
        service
    ):

        result = subprocess.run(
            [
                "systemctl",
                "is-active",
                service
            ],
            capture_output=True,
            text=True
        )

        status = result.stdout.strip()

        self.status_labels[
            service
        ].setText(status)

    # =========================================================
    # FIREWALL LOGIC
    # =========================================================

    def add_rule(self):

        proto = self.proto_box.currentText()

        port = self.port_input.text().strip()

        action = self.action_box.currentText()

        src_ip = self.ip_filter_input.text().strip()

        if not validate_port(port):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid Port"
            )

            return

        if src_ip and not validate_ip(
            src_ip
        ):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid IP"
            )

            return

        cmd = [
            "sudo",
            "iptables",
            "-I",
            "INPUT",
            "1"
        ]

        if src_ip:
            cmd += ["-s", src_ip]

        cmd += [
            "-p",
            proto,
            "--dport",
            port
        ]

        if action == "REJECT":

            cmd += [
                "-j",
                "REJECT",
                "--reject-with",
                "icmp-port-unreachable"
            ]

        else:

            cmd += [
                "-j",
                action
            ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            QMessageBox.information(
                self,
                "Success",
                "Rule Added"
            )

            self.load_rules()

        else:

            QMessageBox.critical(
                self,
                "Error",
                result.stderr
            )

    def load_rules(self):

        result = subprocess.run(
            [
                "sudo",
                "iptables",
                "-L",
                "INPUT",
                "-n",
                "--line-numbers"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            self.rules_display.setText(
                result.stdout
            )

        else:

            self.rules_display.setText(
                result.stderr
            )

    def flush_rules(self):

        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Flush all INPUT rules?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:

            subprocess.run(
                [
                    "sudo",
                    "iptables",
                    "-F",
                    "INPUT"
                ],
                capture_output=True
            )

            self.load_rules()

    def export_rules(self):

        result = subprocess.run(
            [
                "sudo",
                "iptables-save"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            with open(
                "firewall_backup.rules",
                "w"
            ) as f:

                f.write(result.stdout)

            QMessageBox.information(
                self,
                "Saved",
                "Rules exported"
            )

    def block_ip(self):

        ip = self.block_ip_input.text().strip()

        if not validate_ip(ip):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid IP"
            )

            return

        subprocess.run(
            [
                "sudo",
                "iptables",
                "-I",
                "INPUT",
                "1",
                "-s",
                ip,
                "-j",
                "DROP"
            ]
        )

        self.load_rules()

    def unblock_ip(self):

        ip = self.block_ip_input.text().strip()

        if not validate_ip(ip):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid IP"
            )

            return

        subprocess.run(
            [
                "sudo",
                "iptables",
                "-D",
                "INPUT",
                "-s",
                ip,
                "-j",
                "DROP"
            ]
        )

        self.load_rules()

    def allow_ip(self):

        ip = self.allow_ip_input.text().strip()

        if not validate_ip(ip):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid IP"
            )

            return

        subprocess.run(
            [
                "sudo",
                "iptables",
                "-I",
                "INPUT",
                "1",
                "-s",
                ip,
                "-j",
                "ACCEPT"
            ]
        )

        self.load_rules()

    def run_nmap(self):

        ip = self.nmap_ip_input.text().strip()

        if not validate_ip(ip):

            QMessageBox.warning(
                self,
                "Error",
                "Invalid IP"
            )

            return

        result = subprocess.run(
            [
                "nmap",
                "-Pn",
                ip
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            self.nmap_result.setText(
                result.stdout
            )

        else:

            self.nmap_result.setText(
                result.stderr
            )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = PortShieldGUI()

    window.show()

    sys.exit(app.exec())
