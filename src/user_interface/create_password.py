"""A module that contains the CreatePassword class
"""
from pathlib2 import Path
from PyQt6.QtCore import QPointF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.user_interface.ok_alert import OkAlert
from src.secure import Secure


class CreatePassword(QWidget):
    """A class that run create password window of the password manager application."""

    submit_clicked = pyqtSignal(bool)

    def __init__(
        self,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.mouse_old_position = QPointF(0, 0)
        self.ok_alert_window = 0
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.show()
        first_part = "It appears that this is your first time using this application."
        second_part = "Welcome, we hope you have a great experience."
        third_part = "It needed to select a master password to start. keep it secure."
        self.show_ok_alert_window(f"{first_part}\n{second_part}\n{third_part}")

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Change Password"
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
        self.minimize_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["minimize"]))), ""
        )
        self.minimize_pushbutton.clicked.connect(self.showMinimized)
        self.app_buttons_layout.addWidget(self.minimize_pushbutton)
        self.maximize_or_restore_down_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["expand"]))), ""
        )
        self.maximize_or_restore_down_pushbutton.clicked.connect(
            self.maximize_or_restore
        )
        self.app_buttons_layout.addWidget(self.maximize_or_restore_down_pushbutton)
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
        self.password_layout = QHBoxLayout()
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setPlaceholderText("Password")
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_layout.addWidget(self.password_line_edit)
        self.password_show_or_hide_button = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["show"]))), ""
        )
        self.password_show_or_hide_button.setMinimumHeight(24)
        self.password_show_or_hide_button.clicked.connect(self.show_or_hide_password)
        self.password_layout.addWidget(self.password_show_or_hide_button)
        self.main_window_layout.addLayout(self.password_layout)

        self.confirm_password_layout = QHBoxLayout()
        self.confirm_password_line_edit = QLineEdit()
        self.confirm_password_line_edit.setPlaceholderText("Confirm Password")
        self.confirm_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_layout.addWidget(self.confirm_password_line_edit)
        self.confirm_show_or_hide_button = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["show"]))), ""
        )
        self.confirm_show_or_hide_button.setMinimumHeight(24)
        self.confirm_show_or_hide_button.clicked.connect(
            self.show_or_hide_confirm_password
        )
        self.confirm_password_layout.addWidget(self.confirm_show_or_hide_button)
        self.main_window_layout.addLayout(self.confirm_password_layout)
        self.done_pushbutton = QPushButton("Done")
        self.done_pushbutton.clicked.connect(self.create_password)
        self.main_window_layout.addWidget(self.done_pushbutton)
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

    def show_or_hide_password(self) -> None:
        """A method that run every time show_or_hide_button press.

        this method show or hide password in password_line_edit.
        """
        if self.password_line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.password_show_or_hide_button.setIcon(
                QIcon(str(Path(self.application_data["icons"]["hide"])))
            )
        else:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_show_or_hide_button.setIcon(
                QIcon(str(Path(self.application_data["icons"]["show"])))
            )

    def show_or_hide_confirm_password(self) -> None:
        """A method that run every time show_or_hide_button press.

        this method show or hide password in password_line_edit.
        """
        if self.confirm_password_line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.confirm_password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.confirm_show_or_hide_button.setIcon(
                QIcon(str(Path(self.application_data["icons"]["hide"])))
            )
        else:
            self.confirm_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_show_or_hide_button.setIcon(
                QIcon(str(Path(self.application_data["icons"]["show"])))
            )

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

    def create_password(self) -> None:
        """A method that check if passwords entered correctly,
        then save it and send signal to parent window"""
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        secure = Secure()
        password = self.password_line_edit.text()
        confirm_password = self.confirm_password_line_edit.text()
        if password == confirm_password:
            password_hash = secure.hash_password(password)
            with open(file_path, "wb") as file:
                file.write(password_hash)
            self.submit_clicked.emit(True)
        else:
            self.show_ok_alert_window("password and confirm password are not the same!")
            self.submit_clicked.emit(False)
        self.close_window()

    def show_ok_alert_window(self, message: str) -> None:
        """A method that create ok alert window and connect it to self.ok_alert_window.

        Args:
            message (str): A message that send to the ok alert window to show.
        """
        self.ok_alert_window = OkAlert(message, self.application_data)

    def maximize_or_restore(self) -> None:
        """A method that run whenever maximize or restore buttons pressed.

        this method change the state of the window between maximize mode and default mode.
        """
        if self.isMaximized():
            self.showNormal()
            self.maximize_or_restore_down_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icons"]["expand"])))
            )
        else:
            self.showMaximized()
            self.maximize_or_restore_down_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icons"]["collapse"])))
            )

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
