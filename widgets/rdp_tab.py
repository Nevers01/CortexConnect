import subprocess
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class RdpTab(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.process = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.placeholder = QLabel(f"{server.name} RDP başlatılıyor...")
        self.placeholder.setStyleSheet("padding: 12px; color: #8b949e;")
        layout.addWidget(self.placeholder)

        self.setLayout(layout)

        QTimer.singleShot(500, self.start_rdp)

    def start_rdp(self):
        self.process = subprocess.Popen([
            "xfreerdp",
            f"/v:{self.server.host}:{self.server.port}",
            f"/u:{self.server.username}",
            f"/p:{self.server.password}",
            "/dynamic-resolution",
            "/cert:ignore",
            f"/parent-window:{int(self.winId())}"
        ])

        self.placeholder.hide()

    def close_terminal(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()