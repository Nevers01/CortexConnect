from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton


class Sidebar(QFrame):
    def __init__(self, on_add_server, on_refresh):
        super().__init__()

        self.on_add_server = on_add_server
        self.on_refresh = on_refresh

        self.setObjectName("Sidebar")
        self.setFixedWidth(260)

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 24, 22, 24)

        title = QLabel("Cortex Connect")
        title.setObjectName("Title")

        subtitle = QLabel("Remote Station")
        subtitle.setObjectName("SubTitle")

        dashboard_btn = QPushButton("🏠 Dashboard")
        servers_btn = QPushButton("🖥 Sunucular")
        files_btn = QPushButton("📁 Dosyalar")
        settings_btn = QPushButton("⚙ Ayarlar")

        add_btn = QPushButton("➕ Sunucu Ekle")
        add_btn.setObjectName("Blue")
        add_btn.clicked.connect(self.on_add_server)

        refresh_btn = QPushButton("🔄 Yenile")
        refresh_btn.clicked.connect(self.on_refresh)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(24)

        layout.addWidget(dashboard_btn)
        layout.addWidget(servers_btn)
        layout.addWidget(files_btn)
        layout.addWidget(settings_btn)

        layout.addSpacing(24)
        layout.addWidget(add_btn)
        layout.addWidget(refresh_btn)

        layout.addStretch()

        footer = QLabel("Cortex ThinClient v0.3.4")
        footer.setObjectName("SubTitle")
        layout.addWidget(footer)

        self.setLayout(layout)
