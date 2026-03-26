from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QTextDocument, QFont


class WrappingLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setWordWrap(True)
        self.setTextFormat(Qt.TextFormat.RichText)

        # Emoji-capable font stack
        font = QFont()
        font.setFamilies([
            "Segoe UI Emoji",
            "Apple Color Emoji",
            "Noto Color Emoji",
            "Arial"
        ])
        font.setPointSize(10)
        self.setFont(font)

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.MinimumExpanding
        )

    def heightForWidth(self, width: int) -> int:
        doc = QTextDocument()
        doc.setDefaultFont(self.font())
        doc.setHtml(self.text())
        doc.setTextWidth(max(width, 1))
        return int(doc.size().height()) + 4

    def hasHeightForWidth(self):
        return True

    def sizeHint(self):
        base = super().sizeHint()
        return QSize(base.width(), self.heightForWidth(base.width()))


class MessageBubble(QWidget):
    def __init__(self, sender, text, timestamp, is_me=False):
        super().__init__()

        self.outer_layout = QHBoxLayout(self)
        self.outer_layout.setContentsMargins(12, 4, 12, 4)

        # Always create container
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 6, 10, 6)
        self.container_layout.setSpacing(3)

        # ================= SYSTEM MESSAGE =================
        if sender == "System":
            self.container.setStyleSheet("""
                QWidget {
                    background-color: #e5e5ea;
                    border-radius: 10px;
                }
            """)

            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    color: black;
                    font-size: 13px;
                    background: transparent;
                }
            """)

            time_label = QLabel(timestamp)
            time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            time_label.setStyleSheet("""
                QLabel {
                    color: #444;
                    font-size: 10px;
                    background: transparent;
                }
            """)

            self.container_layout.addWidget(label)
            self.container_layout.addWidget(time_label)

            self.outer_layout.addStretch()
            self.outer_layout.addWidget(self.container)
            self.outer_layout.addStretch()
            return

        # ================= USER MESSAGE =================
        bubble_color = "#dcf8c6" if is_me else "#ffffff"

        if is_me:
            self.container.setStyleSheet(f"""
                QWidget {{
                    background-color: {bubble_color};
                    border-radius: 12px;
                    border-top-right-radius: 0px;
                }}
            """)
        else:
            self.container.setStyleSheet(f"""
                QWidget {{
                    background-color: {bubble_color};
                    border-radius: 12px;
                    border-top-left-radius: 0px;
                }}
            """)

        # Sender name
        sender_label = QLabel(sender)
        sender_label.setStyleSheet("""
            QLabel {
                color: #075e54;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }
        """)
        sender_label.setAlignment(
            Qt.AlignmentFlag.AlignRight if is_me else Qt.AlignmentFlag.AlignLeft
        )
        self.container_layout.addWidget(sender_label)

        # Escape HTML safely
        safe_text = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

        html = f"""
        <div style="
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: anywhere;
            line-height: 120%;
        ">{safe_text}</div>
        """

        self.label = WrappingLabel(html)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #111;
                background: transparent;
            }
        """)
        self.container_layout.addWidget(self.label)

        # Timestamp
        time_label = QLabel(timestamp)
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        time_label.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 11px;
                background: transparent;
            }
        """)
        self.container_layout.addWidget(time_label)

        # Alignment
        if is_me:
            self.outer_layout.addStretch()
            self.outer_layout.addWidget(self.container)
        else:
            self.outer_layout.addWidget(self.container)
            self.outer_layout.addStretch()

    # 🔥 UPDATED WIDTH (wider bubbles)
    def update_width(self, parent_width):
        max_width = int(parent_width * 0.72)  # increased from 0.6 → 0.72
        self.container.setMaximumWidth(max_width)