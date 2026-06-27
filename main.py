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
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 24, 22, 24)

        title = QLabel("Cortex Connect")
        title.setObjectName("Title")

        subtitle = QLabel("Remote Station")
        subtitle.setObjectName("SubTitle")

        add_btn = QPushButton("+ Sunucu Ekle")
        add_btn.setObjectName("Blue")
        add_btn.clicked.connect(self.add_server)

        refresh_btn = QPushButton("Yenile")
        refresh_btn.clicked.connect(self.load_servers)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(24)
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)
        layout.addStretch()

        footer = QLabel("Cortex ThinClient v0.1")
        footer.setObjectName("SubTitle")
        layout.addWidget(footer)

        sidebar.setLayout(layout)
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

        card = QFrame()
        card.setObjectName("Card")

        layout = QHBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)

        icon = {
            "SSH": "💻",
            "RDP": "🖥️",
            "VNC": "📺"
        }.get(server.type, "🌐")

        online = ping_host(server.host)

        status = "🟢 Online" if online else "🔴 Offline"

        info = QLabel(f"""
            <b>{icon} {server.name}</b>
            <br>
            {server.type}
            <br>
            👤 {server.username}
            <br>
            🌐 {server.host}:{server.port}
            <br>
            {status}
            """)

        info.setStyleSheet("""
            font-size:17px;
            padding:5px;
        """)

        connect_btn = QPushButton("Bağlan")
        connect_btn.setObjectName("Blue")
        connect_btn.clicked.connect(lambda: self.connect(server))

        edit_btn = QPushButton("Düzenle")
        edit_btn.clicked.connect(lambda: self.edit_server(server))

        delete_btn = QPushButton("Sil")
        delete_btn.setObjectName("Red")
        delete_btn.clicked.connect(lambda: self.remove_server(server.id, server.name))

        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(connect_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

        card.setLayout(layout)

        return card
    
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
