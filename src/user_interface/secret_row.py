"""A module that contains the SecretRow class
"""

from pyperclip import copy
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton
from pathlib2 import Path

from src.user_interface.edit_item import EditItem


class SecretRow(QHBoxLayout):
    """A class that make a row of secrets in table"""

    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        application_data: dict[str, str],
    ) -> None:
        super().__init__()
        self.name = name
        self.username = username
        self.password = password
        self.application_data = application_data
        self.edit_item_window_ui = 0
        self.setup_ui()

    def setup_ui(self) -> None:
        """This method setup the UI of the window."""
        self.setSpacing(5)
        self.name_line_edit = QLineEdit(f"{self.name}")
        self.name_line_edit.setMinimumHeight(24)
        self.name_line_edit.setDisabled(True)
        self.addWidget(self.name_line_edit)
        self.username_line_edit = QLineEdit(f"{self.username}")
        self.username_line_edit.setMinimumHeight(24)
        self.username_line_edit.setDisabled(True)
        self.addWidget(self.username_line_edit)
        self.password_line_edit = QLineEdit(f"{self.password}")
        self.password_line_edit.setMinimumHeight(24)
        self.password_line_edit.setDisabled(True)
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.addWidget(self.password_line_edit)
        self.show_or_hide_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["show"]))), ""
        )
        self.show_or_hide_pushbutton.setMinimumHeight(24)
        self.show_or_hide_pushbutton.clicked.connect(self.show_or_hide)
        self.addWidget(self.show_or_hide_pushbutton)
        self.copy_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["copy"]))), ""
        )
        self.copy_pushbutton.setMinimumHeight(24)
        self.copy_pushbutton.clicked.connect(self.copy_password_to_clipboard)
        self.addWidget(self.copy_pushbutton)
        self.edit_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["edit"]))), ""
        )
        self.edit_pushbutton.setMinimumHeight(24)
        self.edit_pushbutton.clicked.connect(self.edit_item_window)
        self.addWidget(self.edit_pushbutton)
        self.remove_pushbutton = QPushButton(
            QIcon(str(Path(self.application_data["icons"]["remove"]))), ""
        )
        self.remove_pushbutton.setMinimumHeight(24)
        self.remove_pushbutton.clicked.connect(self.remove_row)
        self.addWidget(self.remove_pushbutton)

    def show_or_hide(self) -> None:
        """A method that show or hide the password."""
        if self.password_line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_or_hide_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icons"]["hide"])))
            )
        else:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_or_hide_pushbutton.setIcon(
                QIcon(str(Path(self.application_data["icons"]["show"])))
            )

    def copy_password_to_clipboard(self) -> None:
        """A method that copy the password into clipboard."""
        if self.password_line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            copy(self.password_line_edit.text())
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            copy(self.password_line_edit.text())

    def remove_row(self) -> None:
        """A method that remove the data in this row of table."""
        self.removeItem(self)
        self.name_line_edit.deleteLater()
        self.username_line_edit.deleteLater()
        self.password_line_edit.deleteLater()
        self.show_or_hide_pushbutton.deleteLater()
        self.copy_pushbutton.deleteLater()
        self.edit_pushbutton.deleteLater()
        self.remove_pushbutton.deleteLater()
        self.deleteLater()

    def edit_item_window(self) -> None:
        """A method that create edit item window and connect it to self.edit_item_window_confirm."""
        self.edit_item_window_ui = EditItem(self.application_data)
        self.edit_item_window_ui.name_line_edit.setText(self.name_line_edit.text())
        self.edit_item_window_ui.username_line_edit.setText(
            self.username_line_edit.text()
        )
        self.edit_item_window_ui.password_line_edit.setText(
            self.password_line_edit.text()
        )
        self.edit_item_window_ui.submit_clicked.connect(self.edit_item_window_confirm)

    def edit_item_window_confirm(self, name, username, password):
        """A method that get data from the edit item window.
        and put the data in line edit widgets.

        Args:
            name (_type_): The name of secret
            username (_type_): The username of secret
            password (_type_): The password of secret
        """
        self.name_line_edit.setText(name)
        self.username_line_edit.setText(username)
        self.password_line_edit.setText(password)
