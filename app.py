import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog,
    QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6 import uic

from PyQt6.QtGui import QIcon
from components.message_bubble import MessageBubble
from components.parser_thread import ParserThread

def center_window(self):
    screen = self.screen().availableGeometry()
    window = self.frameGeometry()

    x = (screen.width() - window.width()) // 2
    y = (screen.height() - window.height()) // 2

    self.move(x, y)

class WhatsAppViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/main.ui", self)

        self.setWindowTitle("WhatsApp Chat Viewer")
        self.actionImport_Chat.triggered.connect(self.import_chat)

        self.bg_pixmap = QPixmap("assets/bg.jpg")

        self.setWindowIcon(QIcon("assets/WP.ico"))
        self.messages = []
        self.users = []
        self.me = None

        # Lazy loading
        self.batch_size = 100
        self.current_index = 0

        self.chatLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chatScroll.verticalScrollBar().valueChanged.connect(self.check_scroll)

        self.setStyleSheet("""
            QWidget#chatContainer { background: transparent; }
            QScrollArea { border: none; background: transparent; }
        """)

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

    # IMPORT
    def import_chat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Chat", "", "*.txt")

        if not file_path:
            return

        self.thread = ParserThread(file_path)
        self.thread.finished.connect(self.on_parsed)
        self.thread.error.connect(lambda e: QMessageBox.critical(self,"Error",e))
        self.thread.start()

    def on_parsed(self, messages):
        self.messages = messages
        self.detect_users()
        self.ask_user()
        self.clear_chat()
        self.current_index = 0
        self.load_batch()

    def detect_users(self):
        self.users = list({m["sender"] for m in self.messages if m["type"]=="user"})

    def ask_user(self):
        user, ok = QInputDialog.getItem(self,"Who are you?","Select:",self.users,0,False)
        self.me = user if ok else self.users[0]

    # LAZY LOAD
    def load_batch(self):
        end = self.current_index + self.batch_size

        for msg in self.messages[self.current_index:end]:
            bubble = MessageBubble(
                sender=msg["sender"],
                text=msg["message"],
                timestamp=msg["timestamp"],
                is_me=(msg["sender"]==self.me)
            )
            bubble.update_width(self.width())
            self.chatLayout.addWidget(bubble)

        self.current_index = end

    def check_scroll(self):
        bar = self.chatScroll.verticalScrollBar()
        if bar.value() >= bar.maximum()-20:
            if self.current_index < len(self.messages):
                self.load_batch()

    def clear_chat(self):
        for i in reversed(range(self.chatLayout.count())):
            w = self.chatLayout.itemAt(i).widget()
            if w:
                w.deleteLater()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for i in range(self.chatLayout.count()):
            w = self.chatLayout.itemAt(i).widget()
            if isinstance(w, MessageBubble):
                w.update_width(self.width())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppViewer()
    window.show()
    sys.exit(app.exec())