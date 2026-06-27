import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QMessageBox,
)
from PyQt6.QtCore import Qt

import db
from services.connection import open_connection
from dialogs.server_dialog import ServerDialog
from services.status import ping_host
from widgets.sidebar import Sidebar
from widgets.server_card import ServerCard
from styles import APP_STYLE


class CortexConnect(QWidget):
    def __init__(self):
        super().__init__()
        db.init_db()

        self.setWindowTitle("Cortex Connect")
        self.resize(1100, 680)
        self.setMinimumSize(900, 560)
        self.setStyleSheet(APP_STYLE)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.build_sidebar()
        self.build_content()

        self.setLayout(self.main_layout)
        self.load_servers()

    def build_sidebar(self):
        sidebar = Sidebar(on_add_server=self.add_server, on_refresh=self.load_servers)

        self.main_layout.addWidget(sidebar)

    def build_content(self):
        wrapper = QVBoxLayout()
        wrapper.setContentsMargins(26, 26, 26, 26)

        header = QLabel("Sunucular")
        header.setObjectName("Title")

        desc = QLabel("SSH, RDP ve VNC bağlantılarını tek ekrandan yönet.")
        desc.setObjectName("SubTitle")

        self.server_layout = QVBoxLayout()
        self.server_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.server_layout.setSpacing(14)

        scroll_content = QWidget()
        scroll_content.setLayout(self.server_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        wrapper.addWidget(header)
        wrapper.addWidget(desc)
        wrapper.addSpacing(16)
        wrapper.addWidget(scroll)

        self.main_layout.addLayout(wrapper)

    def load_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        servers = db.get_servers()

        if not servers:
            empty = QLabel("Henüz sunucu yok. Sol taraftan + Sunucu Ekle.")
            empty.setObjectName("SubTitle")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.server_layout.addWidget(empty)
            return

        for server in servers:
            self.server_layout.addWidget(self.create_server_card(server))

    def create_server_card(self, server):
        online = ping_host(server.host)

        return ServerCard(
            server=server,
            is_online=online,
            on_connect=self.connect,
            on_edit=self.edit_server,
            on_delete=self.remove_server,
        )

    def add_server(self):
        dialog = ServerDialog(self)

        if dialog.exec():
            data = dialog.get_data()
            db.add_server(
                data["name"],
                data["type"],
                data["host"],
                data["port"],
                data["username"],
                data["password"],
                data["notes"],
            )
            self.load_servers()

    def edit_server(self, server):
        dialog = ServerDialog(self, server)

        if dialog.exec():
            data = dialog.get_data()
            db.update_server(
                server[0],
                data["name"],
                data["type"],
                data["host"],
                data["port"],
                data["username"],
                data["password"],
                data["notes"],
            )
            self.load_servers()

    def remove_server(self, sid, name):
        answer = QMessageBox.question(self, "Silinsin mi?", f"{name} silinsin mi?")

        if answer == QMessageBox.StandardButton.Yes:
            db.delete_server(sid)
            self.load_servers()

    def connect(self, server):
        try:
            open_connection(server)
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CortexConnect()
    window.show()
    sys.exit(app.exec())
