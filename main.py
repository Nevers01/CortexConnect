import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

import db
from pages.servers_page import ServersPage
from widgets.sidebar import Sidebar
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

        self.servers_page = ServersPage()

        self.sidebar = Sidebar(
            on_add_server=self.servers_page.add_server,
            on_refresh=self.servers_page.load_servers
        )

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.servers_page)

        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CortexConnect()
    window.show()
    sys.exit(app.exec())