from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit

from widgets.terminal.ansi_parser import ansi_to_html


class TerminalWidget(QTextEdit):
    data_entered = pyqtSignal(bytes)

    KEY_SEQUENCES = {
        Qt.Key.Key_Up: b"\x1b[A",
        Qt.Key.Key_Down: b"\x1b[B",
        Qt.Key.Key_Right: b"\x1b[C",
        Qt.Key.Key_Left: b"\x1b[D",
        Qt.Key.Key_Home: b"\x1b[H",
        Qt.Key.Key_End: b"\x1b[F",
        Qt.Key.Key_Delete: b"\x1b[3~",
        Qt.Key.Key_PageUp: b"\x1b[5~",
        Qt.Key.Key_PageDown: b"\x1b[6~",
        Qt.Key.Key_Insert: b"\x1b[2~",
        Qt.Key.Key_Tab: b"\t",
        Qt.Key.Key_Backspace: b"\x7f",
        Qt.Key.Key_Return: b"\r",
        Qt.Key.Key_Enter: b"\r",
        Qt.Key.Key_Escape: b"\x1b",
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setReadOnly(True)
        self.setAcceptRichText(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursorWidth(2)

        self.setStyleSheet("""
            QTextEdit {
                background-color: #050505;
                color: #d0d7de;
                border: none;
                padding: 10px;
                font-family: "DejaVu Sans Mono", "Liberation Mono", monospace;
                font-size: 13px;
                selection-background-color: #264f78;
            }
        """)

    def append_terminal_output(self, text: str):
        html_text = ansi_to_html(text)

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml(html_text)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def keyPressEvent(self, event: QKeyEvent):
        modifiers = event.modifiers()
        key = event.key()

        # Terminal kopyalama: Ctrl+Shift+C
        if (
            modifiers & Qt.KeyboardModifier.ControlModifier
            and modifiers & Qt.KeyboardModifier.ShiftModifier
            and key == Qt.Key.Key_C
        ):
            self.copy()
            return

        # Terminal yapıştırma: Ctrl+Shift+V
        if (
            modifiers & Qt.KeyboardModifier.ControlModifier
            and modifiers & Qt.KeyboardModifier.ShiftModifier
            and key == Qt.Key.Key_V
        ):
            clipboard_text = QApplication.clipboard().text()
            if clipboard_text:
                self.data_entered.emit(
                    clipboard_text.encode("utf-8", errors="ignore")
                )
            return

        # Ctrl+A ... Ctrl+Z
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
                control_byte = bytes([key - Qt.Key.Key_A + 1])
                self.data_entered.emit(control_byte)
                return

        sequence = self.KEY_SEQUENCES.get(key)

        if sequence is not None:
            self.data_entered.emit(sequence)
            return

        text = event.text()

        if text:
            self.data_entered.emit(text.encode("utf-8", errors="ignore"))
            return

        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setFocus()