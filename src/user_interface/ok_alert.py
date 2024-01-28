"""A module that contains the OkAlert class
"""
from pathlib2 import Path
from PyQt6.QtCore import QPointF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class OkAlert(QWidget):
    """A class that run alert window with ok button and show a message to user."""

    submit_clicked = pyqtSignal(bool)

    def __init__(
        self,
        message: str,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.message = message
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.mouse_old_position = QPointF(0, 0)
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.show()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Alert"
        window_width = 600
        window_height = 250
        self.setWindowTitle(window_name)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(
            (self.application_data["screen_width"] - window_width) // 2,
            (self.application_data["screen_height"] - window_height) // 2,
            window_width,
            window_height,
        )
        self.setWindowIcon(QIcon(str(Path(self.application_data["icons"]["password"]))))
        self.password_manager_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.app_name_and_icon_layout = QHBoxLayout()
        self.app_icon_label = QLabel("")
        self.app_icon_label.setPixmap(
            QIcon(str(Path(self.application_data["icons"]["password"]))).pixmap(
                QSize(16, 16)
            )
        )
        self.app_name_and_icon_layout.addWidget(self.app_icon_label)
        self.app_nama_label = QLabel("Password Manager")
        self.app_name_and_icon_layout.addWidget(self.app_nama_label)
        self.app_name_and_icon_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.header_layout.addLayout(self.app_name_and_icon_layout)
        self.drag_and_drop_area_layout = QHBoxLayout()
        self.drag_and_drop_area_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.header_layout.addLayout(self.drag_and_drop_area_layout)
        self.app_buttons_layout = QHBoxLayout()
        self.close_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["close"]))), ""
        )
        self.close_pushbutton.clicked.connect(self.close_window)
        self.app_buttons_layout.addWidget(self.close_pushbutton)
        self.app_buttons_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.header_layout.addLayout(self.app_buttons_layout)
        self.password_manager_layout.addLayout(self.header_layout)
        self.main_window_layout = QVBoxLayout()
        self.message_label = QLabel(self.message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_window_layout.addWidget(self.message_label)
        self.ok_pushbutton = QPushButton("Ok")
        self.ok_pushbutton.clicked.connect(self.ok)
        self.main_window_layout.addWidget(self.ok_pushbutton)
        self.password_manager_layout.addLayout(self.main_window_layout)
        self.footer_layout = QHBoxLayout()
        self.status_layout = QHBoxLayout()
        self.time_label = QLabel("00:00:00:00")
        self.status_layout.addWidget(self.time_label)
        self.app_status_label = QLabel("Ready.")
        self.status_layout.addWidget(self.app_status_label)
        self.status_layout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )
        self.footer_layout.addLayout(self.status_layout)
        self.version_layout = QHBoxLayout()
        self.version_label = QLabel(self.application_data["application_version"])
        self.version_layout.addWidget(self.version_label)
        self.version_layout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        )
        self.footer_layout.addLayout(self.version_layout)
        self.auteur_layout = QHBoxLayout()
        self.auteur_icon_label = QLabel("")
        self.auteur_icon_label.setPixmap(
            QIcon(str(Path(self.application_data["images"]["aria_aas"]))).pixmap(
                QSize(16, 16)
            )
        )
        self.auteur_layout.addWidget(self.auteur_icon_label)
        self.auteur_name_label = QLabel("AriAas")
        self.auteur_layout.addWidget(self.auteur_name_label)
        self.auteur_layout.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )
        self.footer_layout.addLayout(self.auteur_layout)
        self.password_manager_layout.addLayout(self.footer_layout)
        self.setLayout(self.password_manager_layout)
        self.setStyleSheet(self.application_data["app_theme"])

    def clock_count(self) -> None:
        """A method that run with self.clock timeout (every 10ms).

        this method calculate hours, minutes, seconds, and milliseconds
        from the time that the window start showing.
        """
        self.clock_counter_variable += 1
        milliseconds = self.clock_counter_variable
        seconds, milliseconds = divmod(milliseconds, 100)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.time_label.setText(
            f"{hours:02}:{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
        )

    def ok(self) -> None:
        """A method that run when ok button pressed.
        send signal to parent window and close itself."""
        self.submit_clicked.emit(True)
        self.close_window()

    def close_window(self) -> None:
        """A method for closing the window"""
        self.close()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """An event handler that run every time mouse pressed and put
        the location of the mouse in a variable.

        Args:
            a0 (QMouseEvent): The event

        Returns:
            super: super().mousePressEvent(a0)
        """
        self.mouse_old_position = a0.globalPosition()
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        """An event handler that run every time mouse pressed and move.
        this event handler made an area on top bar of the window for moving the window.

        Args:
            a0 (QMouseEvent): The event

        Returns:
            super: super().mouseMoveEvent(a0)
        """
        if self.mouse_old_position.y() - self.y() < 40:
            delta = QPointF(a0.globalPosition() - self.mouse_old_position)
            self.move(int(self.x() + delta.x()), int(self.y() + delta.y()))
            self.mouse_old_position = a0.globalPosition()
        return super().mouseMoveEvent(a0)
