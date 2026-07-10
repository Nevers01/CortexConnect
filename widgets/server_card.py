from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class ServerCard(QFrame):
    def __init__(self, server, is_online, on_connect, on_edit, on_delete):
        super().__init__()

        self.server = server
        self.setObjectName("Card")

        layout = QHBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)

        icon = {"SSH": "[SSH]", "RDP": "[RDP]", "VNC": "[VNC]"}.get(
            server.type, "[SRV]"
        )

        status = "🟢 Online" if is_online else "🔴 Offline"

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
            font-size: 17px;
            padding: 5px;
        """)

        connect_btn = QPushButton("Bağlan")
        connect_btn.setObjectName("Blue")
        connect_btn.clicked.connect(lambda: on_connect(server))

        edit_btn = QPushButton("Düzenle")
        edit_btn.clicked.connect(lambda: on_edit(server))

        delete_btn = QPushButton("Sil")
        delete_btn.setObjectName("Red")
        delete_btn.clicked.connect(lambda: on_delete(server.id, server.name))

        layout.addWidget(info)
        layout.addStretch()
        layout.addWidget(connect_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)

        self.setLayout(layout)
