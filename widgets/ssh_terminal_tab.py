import subprocess
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class SshTerminalTab(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.process = None

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.placeholder = QLabel(f"{server.name} SSH terminali başlatılıyor...", self.container)
        self.placeholder.setStyleSheet("padding: 12px; color: #8b949e;")

        layout.addWidget(self.container, 1)
        self.setLayout(layout)

        QTimer.singleShot(800, self.start_terminal)

    def start_terminal(self):
        cmd = (
            f"ssh "
            f"-o ServerAliveInterval=30 "
            f"-o ServerAliveCountMax=120 "
            f"-o TCPKeepAlive=yes "
            f"-p {self.server.port} "
            f"{self.server.username}@{self.server.host}"
        )

        self.process = subprocess.Popen([
            "xterm",
            "-into", str(int(self.container.winId())),
            "-geometry", "200x60",
            "-fa", "Monospace",
            "-fs", "11",
            "-bg", "black",
            "-fg", "white",
            "-T", self.server.name,
            "-e", cmd
        ])

        self.placeholder.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.resize(self.size())

    def close_terminal(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()