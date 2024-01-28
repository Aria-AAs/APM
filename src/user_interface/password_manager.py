"""A module that contains the PasswordManager class
"""
from ast import literal_eval
import os
from pathlib2 import Path
from PyQt6.QtCore import QPointF, QSize, Qt, QTimer
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.user_interface.add_new_item import AddNewItem
from src.user_interface.ok_alert import OkAlert
from src.user_interface.setting import Setting
from src.user_interface.secret_row import SecretRow
from src.user_interface.login import Login
from src.secure import Secure


class PasswordManager(QWidget):
    """A class that run main window of the password manager application."""

    def __init__(
        self,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.login_attempts = 0
        self.is_login_valid = False
        self.reset_factory_signal = False
        self.mouse_old_position = QPointF(0, 0)
        self.setting_window_ui = 0
        self.add_new_item_window_ui = 0
        self.ok_alert_window = 0
        self.password = ""
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.show_login_window()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Password Manager"
        window_width = 1000
        window_height = 800
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
        self.setting_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["setting"]))),
            "Setting",
        )
        self.setting_pushbutton.clicked.connect(self.show_setting_window)
        self.main_window_layout.addWidget(self.setting_pushbutton)
        self.app_header_layout = QHBoxLayout()
        self.name_header_label = QLabel("Name")
        self.app_header_layout.addWidget(self.name_header_label)
        self.username_header_label = QLabel("Username")
        self.app_header_layout.addWidget(self.username_header_label)
        self.password_header_label = QLabel("Password")
        self.app_header_layout.addWidget(self.password_header_label)
        self.add_new_item_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["add_new"]))),
            "Add new item",
        )
        self.add_new_item_pushbutton.clicked.connect(self.show_add_new_item_window)
        self.add_new_item_pushbutton.setMaximumWidth(140)
        self.app_header_layout.addWidget(self.add_new_item_pushbutton)
        self.main_window_layout.addLayout(self.app_header_layout)
        self.app_scroll_area = QScrollArea()
        self.app_scroll_area_layout = QVBoxLayout()
        self.app_scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.app_scroll_area.setLayout(self.app_scroll_area_layout)
        self.main_window_layout.addWidget(self.app_scroll_area)
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

    def maximize_or_restore(self) -> None:
        """A method that run whenever maximize or restore buttons pressed.

        this method change the state of the window between maximize mode and default mode.
        """
        if self.isMaximized():
            self.showNormal()
            self.maximize_or_restore_down_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icon"]["expand"])))
            )
        else:
            self.showMaximized()
            self.maximize_or_restore_down_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icon"]["collapse"])))
            )

    def show_add_new_item_window(self) -> None:
        """A method that create add new item window
        and connect it to self.add_new_item_window_ui."""
        self.add_new_item_window_ui = AddNewItem(self.application_data)
        self.add_new_item_window_ui.submit_clicked.connect(
            self.add_new_item_window_confirm
        )

    def add_new_item_window_confirm(
        self, name: str, username: str, password: str
    ) -> None:
        """A method that make new row in the password manager application.

        Args:
            name (str): The name of the secret
            username (str): username of the secret
            password (str): password of the secret
        """
        self.app_scroll_area_layout.addLayout(
            SecretRow(name, username, password, self.application_data)
        )

    def show_setting_window(self) -> None:
        """A method that create setting window and connect it to self.setting_window_ui."""
        self.close()
        self.setting_window_ui = Setting(self.application_data)
        self.setting_window_ui.submit_clicked.connect(self.setting_window_confirm)

    def setting_window_confirm(self, return_string) -> None:
        """A method that get confirmation of the setting window.

        if is_ok_pressed is true it means the ok button pressed.
        so this method close the application and run it again to apply new settings.
        if is_ok_pressed is false it means the cancel button or close button pressed.
        so this method show the password manager window without any change.

        Args:
            is_ok_pressed (bool): An boolean variable that say is ok button pressed or not.
        """
        if return_string == "ok_pressed":
            self.close_window()
            os.system("python main.py")
        elif return_string == "reset_factory":
            self.reset_factory_signal = True
            self.close_window()
            os.system("python main.py")
        elif return_string == "cancel_pressed":
            self.show()
        else:
            self.close_window()

    def show_ok_alert_window(self, message: str) -> None:
        """A method that create ok alert window and connect it to self.ok_alert_window.

        Args:
            message (str): A message that send to the ok alert window to show.
        """
        self.ok_alert_window = OkAlert(message, self.application_data)

    def show_login_window(self) -> None:
        """A method that create login window and connect it to self.login_window_confirm."""
        self.login_window = Login(self.application_data)
        self.login_window.submit_clicked.connect(self.login_window_confirm)

    def login_window_confirm(self, is_login_valid: bool, password: str) -> None:
        """A method to confirm that the login is valid or not.

        if login is valid then show the main window of password manager application.
        if login is not valid then count and let user try again for three times.

        Args:
            is_login_valid (bool): A boolean variable that say is login valid or not.
        """
        if is_login_valid:
            self.is_login_valid = True
            self.password = password
            self.show()
            self.load_secrets()
        else:
            self.login_attempts += 1
            if self.login_attempts == 3:
                first_part = "You did enter the wrong password three times!"
                second_part = "The application did reset factory."
                self.show_ok_alert_window(f"{first_part}\n{second_part}")
                self.close()
            else:
                self.show_login_window()

    def load_secrets(self) -> None:
        """load secrets from secrets.json file"""
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["secrets_file_name"],
        )
        if not Path.is_file(file_path):
            with open(file_path, "wb") as file:
                file.write(b"")
        else:
            with open(file_path, "rb") as file:
                salt = file.read(32)
                initialization_vector = file.read(16)
                cipher_data = file.read()
            if not initialization_vector == b"":
                secure = Secure()
                key, _ = secure.generate_encryption_key(self.password, salt)
                data = secure.decrypt_data(cipher_data, key, initialization_vector)
                secrets = literal_eval(data)
                for row in secrets:
                    self.app_scroll_area_layout.addLayout(
                        SecretRow(
                            secrets[row]["name"],
                            secrets[row]["username"],
                            secrets[row]["password"],
                            self.application_data,
                        )
                    )

    def save_secrets(self) -> None:
        """save secrets in secrets.json file"""
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["secrets_file_name"],
        )
        secrets = {}
        row_number = 1
        for row in self.app_scroll_area_layout.children():
            secrets[f"row-{row_number}"] = {}
            secrets[f"row-{row_number}"]["name"] = row.name_line_edit.text()
            secrets[f"row-{row_number}"]["username"] = row.username_line_edit.text()
            secrets[f"row-{row_number}"]["password"] = row.password_line_edit.text()
            row_number += 1
        secure = Secure()
        encryption_key, salt = secure.generate_encryption_key(self.password)
        cipher_data, initialization_vector = secure.encrypt_data(
            str(secrets), encryption_key
        )
        with open(file_path, "wb") as file:
            file.write(salt)
            file.write(initialization_vector)
            file.write(cipher_data)

    def close_window(self) -> None:
        """A method that save secrets if login is valid and close the window"""
        if self.is_login_valid and not self.reset_factory_signal:
            self.save_secrets()
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
