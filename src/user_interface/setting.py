"""A module that contains the Setting class
"""
import json
from pathlib2 import Path
from PyQt6.QtCore import QPointF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QStyleFactory,
)

from src.user_interface.change_password import ChangePassword
from src.secure import Secure


class Setting(QWidget):
    """A class that run setting window of the password manager application."""

    submit_clicked = pyqtSignal(str)

    def __init__(
        self,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.mouse_old_position = QPointF(0, 0)
        self.change_password_window = 0
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.show()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Setting"
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
        self.close_pushbutton.clicked.connect(self.cancel)
        self.app_buttons_layout.addWidget(self.close_pushbutton)
        self.app_buttons_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.header_layout.addLayout(self.app_buttons_layout)
        self.password_manager_layout.addLayout(self.header_layout)
        self.main_window_layout = QVBoxLayout()
        self.theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Theme:")
        self.theme_layout.addWidget(self.theme_label)
        self.theme_combo_box = QComboBox()
        self.theme_combo_box.addItem("System")
        self.theme_combo_box.addItem("Dark")
        self.theme_combo_box.addItem("Light")
        self.theme_combo_box.setCurrentText(self.application_data["app_theme"])
        self.theme_layout.addWidget(self.theme_combo_box)
        self.main_window_layout.addLayout(self.theme_layout)
        self.app_style_layout = QHBoxLayout()
        self.app_style_label = QLabel("App Style:")
        self.app_style_layout.addWidget(self.app_style_label)
        self.app_style_combo_box = QComboBox()
        for style in QStyleFactory.keys():
            if style == "Fusion":
                self.app_style_combo_box.addItem("Fusion")
            elif style == "Windows":
                self.app_style_combo_box.addItem("Windows")
            elif style == "windowsvista":
                self.app_style_combo_box.addItem("Windows Vista")
            elif style == "WindowsXP":
                self.app_style_combo_box.addItem("Windows XP")
            elif style == "QtCurve":
                self.app_style_combo_box.addItem("QtCurve")
            elif style == "Oxygen":
                self.app_style_combo_box.addItem("Oxygen")
            elif style == "Breeze":
                self.app_style_combo_box.addItem("Breeze")
            elif style == "Android":
                self.app_style_combo_box.addItem("Android")
            elif style == "Macintosh":
                self.app_style_combo_box.addItem("Macintosh")
        self.app_style_combo_box.setCurrentText(self.application_data["app_style"])
        self.app_style_layout.addWidget(self.app_style_combo_box)
        self.main_window_layout.addLayout(self.app_style_layout)
        self.change_password_pushbutton = QPushButton("Change Main Password")
        self.change_password_pushbutton.clicked.connect(self.change_password)
        self.main_window_layout.addWidget(self.change_password_pushbutton)
        self.reset_factory_pushbutton = QPushButton("Reset Factory")
        self.reset_factory_pushbutton.clicked.connect(self.reset_factory)
        self.main_window_layout.addWidget(self.reset_factory_pushbutton)
        self.submit_pushbuttons_layout = QHBoxLayout()
        self.submit_pushbuttons_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.ok_pushbutton = QPushButton("Ok")
        self.ok_pushbutton.clicked.connect(self.ok)
        self.submit_pushbuttons_layout.addWidget(self.ok_pushbutton)
        self.cancel_pushbutton = QPushButton("Cancel")
        self.cancel_pushbutton.clicked.connect(self.cancel)
        self.submit_pushbuttons_layout.addWidget(self.cancel_pushbutton)
        self.main_window_layout.addLayout(self.submit_pushbuttons_layout)
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
        self.setStyleSheet(self.application_data["app_theme"])

    def change_password(self) -> None:
        """A method that create password change window and
        connect it to self.change_password_window_confirm."""
        self.change_password_window = ChangePassword(self.application_data)
        self.change_password_window.submit_clicked.connect(
            self.change_password_window_confirm
        )

    def change_password_window_confirm(self, return_code, new_password) -> None:
        """A method that get confirmation of the password change window.

        if return_code is 0 it means the password changed correctly.
        so this method save new password that is in new_password variable.
        if return_code is 1 it means the new entered password is not match with confirm one.
        nothing to do.
        if return_code is 2 it means the old password does not entered correctly.
        close the application for safety.

        Args:
            return_code (int): An integer variable that say state of confirmation.
            new_password (str): A string variable that contains the new password.
        """
        if return_code == 0:
            self.save_new_password(new_password)
        elif return_code in (1, 3):
            self.close_window()

    def save_new_password(self, new_password) -> None:
        """A method to save new password in main_password.json file

        Args:
            new_password (str): the new password that we want to save.
        """
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        secure = Secure()
        with open(file_path, "wb") as file:
            file.write(secure.hash_password(new_password))
        self.close_window()

    def save_setting_data(self) -> None:
        """save the setting data to setting.json file"""
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["settings_file_name"],
        )
        data = {}
        data["app_style"] = self.app_style_combo_box.currentText()
        data["app_theme"] = self.theme_combo_box.currentText()
        with open(file_path, "wt", encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

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

    def reset_factory(self) -> None:
        """A method that clear and delete the data of the application and restart it"""
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        with open(file_path, "wb") as file:
            file.write(b"")
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["secrets_file_name"],
        )
        with open(file_path, "wb") as file:
            file.write(b"")
        self.close_window()
        self.submit_clicked.emit("reset_factory")

    def ok(self) -> None:
        """Send a True to parent window."""
        self.save_setting_data()
        self.close_window()
        self.submit_clicked.emit("ok_pressed")

    def cancel(self) -> None:
        """Send a False to parent window."""
        self.close_window()
        self.submit_clicked.emit("cancel_pressed")

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
