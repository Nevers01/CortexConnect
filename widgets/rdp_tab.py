import subprocess
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class RdpTab(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.process = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.placeholder = QLabel(f"{server.name} RDP başlatılıyor...", self.container)
        self.placeholder.setStyleSheet("padding: 12px; color: #8b949e;")

        layout.addWidget(self.container, 1)
        self.setLayout(layout)

        QTimer.singleShot(800, self.start_rdp)

    def start_rdp(self):
        width = max(self.container.width(), 1024)
        height = max(self.container.height(), 768)

        self.process = subprocess.Popen([
            "xfreerdp",
            f"/v:{self.server.host}:{self.server.port}",
            f"/u:{self.server.username}",
            f"/p:{self.server.password}",
            f"/w:{width}",
            f"/h:{height}",
            "/cert:ignore",
            f"/parent-window:{int(self.container.winId())}"
        ])

        self.placeholder.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.resize(self.size())

    def close_terminal(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()