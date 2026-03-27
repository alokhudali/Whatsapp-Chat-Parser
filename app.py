import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog,
    QMessageBox, QInputDialog, QLabel, QVBoxLayout, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QIcon

from ui.ui_main import Ui_MainWindow
from components.message_bubble import MessageBubble
from components.parser_thread import ParserThread


# Resource path (for PyInstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def center_window(window):
    screen = window.screen().availableGeometry()
    frame = window.frameGeometry()

    x = (screen.width() - frame.width()) // 2
    y = (screen.height() - frame.height()) // 2

    window.move(x, y)


class WhatsAppViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("WhatsApp Chat Viewer")

        # MENU
        self.ui.actionImport_Chat.triggered.connect(self.import_chat)
        self.ui.actionAbout.triggered.connect(self.show_about)

        # Assets
        self.bg_pixmap = QPixmap(resource_path("assets/bg.jpg"))
        self.setWindowIcon(QIcon(resource_path("assets/WP.ico")))

        self.messages = []
        self.users = []
        self.me = None

        # Lazy loading
        self.batch_size = 100
        self.current_index = 0

        self.ui.chatLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ui.chatScroll.verticalScrollBar().valueChanged.connect(self.check_scroll)

        self.setStyleSheet("""
            QWidget#chatContainer { background: transparent; }
            QScrollArea { border: none; background: transparent; }
        """)

        center_window(self)

    # ABOUT POPUP
    def show_about(self):
        dialog = QDialog(self)

        dialog.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        dialog.setWindowTitle("About")
        dialog.setFixedSize(320, 320)

        layout = QVBoxLayout(dialog)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ICON
        icon_label = QLabel()
        pixmap = QPixmap(resource_path("assets/WhatsappParser.png"))
        icon_label.setPixmap(
            pixmap.scaled(
                110, 110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # TITLE
        title = QLabel("WhatsApp Chat Viewer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        # DESCRIPTION
        desc = QLabel(
            "Standalone viewer for WhatsApp chat exports.\n\n"
            "Built with PyQt6\n"
            "Version 1.0"
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addSpacing(10)
        layout.addWidget(title)
        layout.addSpacing(5)
        layout.addWidget(desc)

        dialog.exec()

    # BACKGROUND    
    def paintEvent(self, event):
        painter = QPainter(self)

        if self.bg_pixmap.isNull():
            return

        scaled = self.bg_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (scaled.width() - self.width()) // 2
        y = (scaled.height() - self.height()) // 2

        painter.drawPixmap(0, 0, scaled, x, y, self.width(), self.height())

    # IMPORT CHAT
    def import_chat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Chat", "", "*.txt")

        if not file_path:
            return

        self.thread = ParserThread(file_path)
        self.thread.finished.connect(self.on_parsed)
        self.thread.error.connect(lambda e: QMessageBox.critical(self, "Error", e))
        self.thread.start()

    def on_parsed(self, messages):
        self.messages = messages
        self.detect_users()

        # STOP if user cancels selection
        if not self.ask_user():
            return

        self.clear_chat()
        self.current_index = 0
        self.load_batch()

    # USER SELECTION
    def ask_user(self):
        user, ok = QInputDialog.getItem(
            self,
            "Who are you?",
            "Select:",
            self.users,
            0,
            False
        )

        if not ok:
            return False  # user cancelled

        self.me = user
        return True

    def detect_users(self):
        self.users = list({m["sender"] for m in self.messages if m["type"] == "user"})
  
    # LAZY LOAD
    def load_batch(self):
        end = self.current_index + self.batch_size

        for msg in self.messages[self.current_index:end]:
            bubble = MessageBubble(
                sender=msg["sender"],
                text=msg["message"],
                timestamp=msg["timestamp"],
                is_me=(msg["sender"] == self.me)
            )
            bubble.update_width(self.width())
            self.ui.chatLayout.addWidget(bubble)

        self.current_index = end

    def check_scroll(self):
        bar = self.ui.chatScroll.verticalScrollBar()

        if bar.value() >= bar.maximum() - 20:
            if self.current_index < len(self.messages):
                self.load_batch()

    def clear_chat(self):
        for i in reversed(range(self.ui.chatLayout.count())):
            w = self.ui.chatLayout.itemAt(i).widget()
            if w:
                w.deleteLater()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        for i in range(self.ui.chatLayout.count()):
            w = self.ui.chatLayout.itemAt(i).widget()
            if isinstance(w, MessageBubble):
                w.update_width(self.width())


# RUN APP
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppViewer()
    window.show()
    sys.exit(app.exec())