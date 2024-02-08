"""A module that contains the Login class
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

from src.secure import Secure
from src.user_interface.create_password import CreatePassword


class Login(QWidget):
    """A class that run login window of the password manager application."""

    submit_clicked = pyqtSignal(bool, str)

    def __init__(
        self,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.mouse_old_position = QPointF(0, 0)
        self.secure = Secure()
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.check_if_password_exist()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Login"
        window_width = 400
        window_height = 200
        self.setWindowTitle(window_name)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
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
        self.show_or_hide_button = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["show"]))), ""
        )
        self.show_or_hide_button.setMinimumHeight(24)
        self.show_or_hide_button.clicked.connect(self.show_or_hide)
        self.password_layout.addWidget(self.show_or_hide_button)
        self.main_window_layout.addLayout(self.password_layout)
        self.login_pushbutton_layout = QHBoxLayout()
        self.login_pushbutton = QPushButton("Login")
        self.login_pushbutton.clicked.connect(self.login)
        self.login_pushbutton_layout.addWidget(self.login_pushbutton)
        self.main_window_layout.addLayout(self.login_pushbutton_layout)
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

    def show_or_hide(self) -> None:
        """A method that run every time show_or_hide_button press.

        this method show or hide password in password_line_edit.
        """
        if self.password_line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_or_hide_button.setIcon(
                QIcon(str(Path(self.application_data["icons"]["hide"])))
            )
        else:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_or_hide_button.setIcon(
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

    def check_if_password_exist(self) -> None:
        """A method that check if main_password.key file exist and not empty.
        if it is empty or does not exist make create password window to create the file
        """
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        if not Path.exists(file_path):
            with open(file_path, "wb") as file:
                file.write(b"")
            self.create_password = CreatePassword(self.application_data)
            self.create_password.submit_clicked.connect(self.create_password_confirm)
        else:
            with open(file_path, "rb") as file:
                password = file.read()
                if password == b"":
                    self.create_password = CreatePassword(self.application_data)
                    self.create_password.submit_clicked.connect(
                        self.create_password_confirm
                    )
                else:
                    self.show()

    def create_password_confirm(self, is_password_created: bool):
        """Check if password created. if it does not created close the application.

        Args:
            is_password_created (bool): The signal from child window
        """
        if is_password_created:
            self.show()
        else:
            self.close_window()

    def login(self) -> None:
        """A method for check password correctness.

        if password is correct send a True to parent window.
        if password is not correct send a False to parent window.
        """
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        with open(file_path, "rb") as file:
            password_hash = file.read()
        entered_password = self.password_line_edit.text()
        if self.secure.check_password(entered_password, password_hash):
            self.regenerate_hash_and_save(entered_password)
            self.submit_clicked.emit(True, entered_password)
            self.close_window()
        else:
            self.submit_clicked.emit(False, "")
            self.close_window()

    def regenerate_hash_and_save(self, password: str) -> None:
        """A method that regenerated password hash with new salt and save it.

        Args:
            password (str): the password to regenerated hash.
        """
        file_path = Path(
            self.application_data["data_files_path"],
            self.application_data["main_password_file_name"],
        )
        password_hash = self.secure.hash_password(password)
        with open(file_path, "wb") as file:
            file.write(password_hash)

    def close_window(self) -> None:
        """A method for closing the window"""
        self.close()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """An event handler that run every time mouse pressed and put.
        the location of the mouse in a variable.

        Args:
            a0 (QMouseEvent): The event.

        Returns:
            super: super().mousePressEvent(a0).
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
