from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from services.ssh.session import SSHSession
from widgets.terminal.terminal_widget import TerminalWidget


class SSHTab(QWidget):
    def __init__(self, server):
        super().__init__()

        self.server = server
        self.session = SSHSession(server)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_label = QLabel(
            f"{server.name} sunucusuna bağlanılıyor..."
        )
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #161b22;
                color: #8b949e;
                border-bottom: 1px solid #30363d;
                padding: 7px 10px;
            }
        """)

        self.terminal = TerminalWidget()

        layout.addWidget(self.status_label)
        layout.addWidget(self.terminal, 1)

        self.terminal.data_entered.connect(self.session.send_raw)

        self.session.output_received.connect(
            self.terminal.append_terminal_output
        )
        self.session.error_received.connect(self.on_error)
        self.session.connected.connect(self.on_connected)
        self.session.disconnected.connect(self.on_disconnected)

        QTimer.singleShot(0, self.session.connect)

    def on_connected(self):
        self.status_label.setText(
            f"Bağlı — {self.server.username}@{self.server.host}:{self.server.port}"
        )

        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #0d2818;
                color: #56d364;
                border-bottom: 1px solid #238636;
                padding: 7px 10px;
            }
        """)

        self.terminal.setFocus()
        self.update_terminal_size()

    def on_error(self, message):
        self.status_label.setText(f"SSH hatası: {message}")

        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #3d1117;
                color: #ff7b72;
                border-bottom: 1px solid #da3633;
                padding: 7px 10px;
            }
        """)

    def on_disconnected(self):
        self.status_label.setText("SSH bağlantısı kapandı.")

        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #161b22;
                color: #8b949e;
                border-bottom: 1px solid #30363d;
                padding: 7px 10px;
            }
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_terminal_size()

    def update_terminal_size(self):
        channel = self.session.channel

        if not channel or channel.closed:
            return

        font_metrics = self.terminal.fontMetrics()

        char_width = max(font_metrics.horizontalAdvance("M"), 1)
        char_height = max(font_metrics.height(), 1)

        columns = max(self.terminal.viewport().width() // char_width, 20)
        rows = max(self.terminal.viewport().height() // char_height, 5)

        try:
            channel.resize_pty(width=columns, height=rows)
        except Exception:
            pass

    def close_terminal(self):
        self.session.disconnect()