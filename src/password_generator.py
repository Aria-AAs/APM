"""A module that contains the PasswordGenerator class
"""

from random import randint

from pathlib2 import Path
from pyperclip import copy
from PyQt6.QtCore import QPointF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QMouseEvent
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class PasswordGenerator(QWidget):
    """A class that run password generator window of the password manager application."""

    submit_clicked = pyqtSignal(str)

    def __init__(
        self,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.application_data = application_data
        self.clock_counter_variable = 0
        self.mouse_old_position = QPointF(0, 0)
        self.password_length = 20
        self.include_lowercase_characters = True
        self.include_uppercase_characters = True
        self.include_number_characters = True
        self.include_symbol_characters = True
        self.setup_ui()
        self.clock = QTimer(self)
        self.clock.timeout.connect(self.clock_count)
        self.clock.start(10)
        self.show()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        window_name = "Generate Password"
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

        self.password_length_slider_layout = QHBoxLayout()
        self.password_length_slider_label = QLabel("Password Length:", self)
        self.password_length_slider_layout.addWidget(self.password_length_slider_label)
        self.password_length_slider_number = QLabel(" 00   ", self)
        self.password_length_slider_layout.addWidget(self.password_length_slider_number)
        self.password_length_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.password_length_slider.setMinimum(1)
        self.password_length_slider.setMaximum(50)
        self.password_length_slider.setSingleStep(1)
        self.password_length_slider.valueChanged.connect(self.set_password_length)
        self.password_length_slider.setValue(self.password_length)
        self.password_length_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.password_length_slider.setTickInterval(1)
        self.password_length_slider_layout.addWidget(self.password_length_slider)
        self.password_length_slider_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_window_layout.addLayout(self.password_length_slider_layout)
        self.checkboxes_layout = QHBoxLayout()
        self.left_checkbox_layout = QVBoxLayout()
        self.lowercase_toggle_checkbox = QCheckBox("Lowercase Letters", self)
        self.lowercase_toggle_checkbox.setChecked(self.include_lowercase_characters)
        self.lowercase_toggle_checkbox.stateChanged.connect(self.lowercase_toggle)
        self.left_checkbox_layout.addWidget(self.lowercase_toggle_checkbox)
        self.uppercase_toggle_checkbox = QCheckBox("Uppercase Letters", self)
        self.uppercase_toggle_checkbox.setChecked(self.include_uppercase_characters)
        self.uppercase_toggle_checkbox.stateChanged.connect(self.uppercase_toggle)
        self.left_checkbox_layout.addWidget(self.uppercase_toggle_checkbox)
        self.checkboxes_layout.addLayout(self.left_checkbox_layout)
        self.right_checkbox_layout = QVBoxLayout()
        self.numbers_toggle_checkbox = QCheckBox("Numbers", self)
        self.numbers_toggle_checkbox.setChecked(self.include_number_characters)
        self.numbers_toggle_checkbox.stateChanged.connect(self.numbers_toggle)
        self.right_checkbox_layout.addWidget(self.numbers_toggle_checkbox)
        self.symbols_toggle_checkbox = QCheckBox("Symbols", self)
        self.symbols_toggle_checkbox.setChecked(self.include_symbol_characters)
        self.symbols_toggle_checkbox.stateChanged.connect(self.symbols_toggle)
        self.right_checkbox_layout.addWidget(self.symbols_toggle_checkbox)
        self.checkboxes_layout.addLayout(self.right_checkbox_layout)
        self.main_window_layout.addLayout(self.checkboxes_layout)
        self.buttons_layout = QHBoxLayout()
        self.generate_password_button = QPushButton("Generate", self)
        self.generate_password_button.clicked.connect(self.generate_password)
        self.buttons_layout.addWidget(self.generate_password_button)
        self.done_button = QPushButton("Done", self)
        self.done_button.clicked.connect(self.submit)
        self.buttons_layout.addWidget(self.done_button)
        self.main_window_layout.addLayout(self.buttons_layout)
        self.output_layout = QVBoxLayout()
        self.output = QLabel("click on generate to generate your password", self)
        self.output.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.output_layout.addWidget(self.output)
        self.main_window_layout.addLayout(self.output_layout)

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

    def set_password_length(self, password_length: int) -> None:
        """A method that get an integer value and set it as password length.

        Args:
            password_length (int): The length to set for the password
        """
        self.password_length = password_length
        self.password_length_slider_number.setText(f" {password_length:02d}   ")

    def lowercase_toggle(self) -> None:
        """A method that toggles between want or not want the lowercase characters."""
        self.include_lowercase_characters = not self.include_lowercase_characters

    def uppercase_toggle(self) -> None:
        """A method that toggles between want or not want the uppercase characters."""
        self.include_uppercase_characters = not self.include_uppercase_characters

    def numbers_toggle(self) -> None:
        """A method that toggles between want or not want the number characters."""
        self.include_number_characters = not self.include_number_characters

    def symbols_toggle(self) -> None:
        """A method that toggles between want or not want the symbol characters."""
        self.include_symbol_characters = not self.include_symbol_characters

    def generate_password(self) -> None:
        """A method that generate password base on the wanted characters."""
        charlist = []
        if self.include_number_characters:
            data = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            for i in data:
                charlist.append(i)
        if self.include_uppercase_characters:
            data = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
            ]
            for i in data:
                charlist.append(i)
        if self.include_lowercase_characters:
            data = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
            ]
            for i in data:
                charlist.append(i)
        if self.include_symbol_characters:
            data = [
                "~",
                "`",
                "!",
                "@",
                "#",
                "$",
                "%",
                "^",
                "&",
                "*",
                "(",
                ")",
                "_",
                "-",
                "+",
                "=",
                "{",
                "[",
                "]",
                "}",
                ":",
                ";",
                "'",
                '"',
                "\\",
                "|",
                "<",
                ">",
                ",",
                ".",
                "/",
                "?",
            ]
            for i in data:
                charlist.append(i)
        if len(charlist) == 0:
            self.output.setText(" ")
        else:
            password = ""
            for _ in range(self.password_length):
                index = randint(1, len(charlist)) - 1
                password += charlist[index]
            self.output.setText(password)
            copy(password)

    def submit(self) -> None:
        """A method that send a signal contain generated password to parent window."""
        self.submit_clicked.emit(self.output.text())
        self.close_window()

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
