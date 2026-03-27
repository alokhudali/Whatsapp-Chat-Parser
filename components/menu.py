from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


def show_about(parent, resource_path):
    dialog = QDialog(parent)

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
        pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    )
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # TITLE
    title = QLabel("WhatsApp Chat Viewer")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 16px; font-weight: bold;")

    # DESC
    desc = QLabel(
        "Standalone viewer for WhatsApp chat exports.\n\n"
        "Built with PyQt6\nVersion 1.0"
    )
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    desc.setWordWrap(True)

    layout.addWidget(icon_label)
    layout.addSpacing(10)
    layout.addWidget(title)
    layout.addSpacing(5)
    layout.addWidget(desc)

    dialog.exec()


def show_user_dialog(parent, users):
    dialog = QDialog(parent)

    dialog.setWindowFlags(
        Qt.WindowType.Dialog |
        Qt.WindowType.CustomizeWindowHint |
        Qt.WindowType.WindowTitleHint |
        Qt.WindowType.WindowCloseButtonHint
    )

    dialog.setWindowTitle("Who are you?")
    dialog.setFixedSize(300, 220)

    layout = QVBoxLayout(dialog)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    title = QLabel("Select your name")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 14px; font-weight: bold;")

    combo = QComboBox()
    combo.addItems(users)
    combo.setFixedWidth(200)

    btn = QPushButton("Continue")
    btn.setFixedWidth(120)

    selected_user = {"value": None}

    def confirm():
        selected_user["value"] = combo.currentText()
        dialog.accept()

    btn.clicked.connect(confirm)

    layout.addWidget(title)
    layout.addSpacing(10)
    layout.addWidget(combo, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addSpacing(15)
    layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    result = dialog.exec()

    return result == QDialog.DialogCode.Accepted, selected_user["value"]