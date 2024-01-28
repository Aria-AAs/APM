"""The start point of the password manager application.
"""
import json
from os import makedirs

from pathlib2 import Path
from PyQt6.QtWidgets import QApplication
from screeninfo import get_monitors
import darkdetect

from .user_interface.password_manager import PasswordManager


class Application:
    """The main class of the password manager application"""

    def __init__(self, argv: list[str]) -> None:
        self.application = QApplication(argv)
        self.application_path = Path.cwd()
        self.data_files_path = Path(self.application_path, "data")
        self.theme_files_path = Path(self.data_files_path, "theme")
        application_version = "0.0.0"
        settings_file_name = "settings.json"
        self.icons_file_name = "icons.json"
        self.images_file_name = "images.json"
        secrets_file_name = "secrets.key"
        main_password_file_name = "main_password.key"
        if not Path.exists(self.data_files_path):
            makedirs(self.data_files_path)
        settings = self.load_settings(self.data_files_path, settings_file_name)
        icons = self.load_icons(self.data_files_path, self.icons_file_name)
        images = self.load_images(self.data_files_path, self.images_file_name)
        screen_size = self.find_screen_size()
        app_style = settings["app_style"]
        self.application.setStyle(app_style)
        app_theme_file_name_without_postfix = settings["app_theme"]
        if app_theme_file_name_without_postfix == "System":
            if darkdetect.isDark():
                app_theme_file_name_without_postfix = "Dark"
            else:
                app_theme_file_name_without_postfix = "Light"
        app_theme_file_name = app_theme_file_name_without_postfix + ".qss"
        app_theme = self.load_app_theme(self.theme_files_path, app_theme_file_name)
        application_data = {
            "application_version": application_version,
            "app_style": app_style,
            "app_theme": app_theme,
            "screen_width": screen_size[0],
            "screen_height": screen_size[1],
            "icons": icons,
            "images": images,
            "data_files_path": self.data_files_path,
            "secrets_file_name": secrets_file_name,
            "settings_file_name": settings_file_name,
            "main_password_file_name": main_password_file_name,
        }
        self.login_window = PasswordManager(application_data)

    def load_settings(
        self, data_files_path: Path, settings_file_name: str
    ) -> dict[str, str]:
        """load settings for application.

        Args:
            data_files_path (Path): The path of the data files.
            settings_file_name (str): The name of file of settings.

        Returns:
            dict[str, str]: return a dict settings of the application.
        """
        file_path = Path(data_files_path, settings_file_name)
        if not Path.is_file(file_path):
            with open(file_path, "wt", encoding="UTF-8") as file:
                json.dump({}, file, indent=4)
        with open(file_path, "rt", encoding="UTF-8") as file:
            settings = json.load(file)
        return settings

    def load_icons(self, data_files_path: Path, icons_file_name: str) -> dict[str, str]:
        """load icons for application.

        Args:
            data_files_path (Path): The path of the data files.
            icons_file_name (str): The name of file of icons.

        Returns:
            dict[str, str]: return a dict of location of icons.
        """
        file_path = Path(data_files_path, icons_file_name)
        if not Path.is_file(file_path):
            with open(file_path, "wt", encoding="UTF-8") as file:
                json.dump({}, file, indent=4)
        with open(file_path, "rt", encoding="UTF-8") as file:
            icons = json.load(file)
        return icons

    def load_images(
        self, data_files_path: Path, images_file_name: str
    ) -> dict[str, str]:
        """load images for application.

        Args:
            data_files_path (Path): The path of the data files.
            images_file_name (str): The name of file of images.

        Returns:
            dict[str, str]: return a dict of location of images.
        """
        file_path = Path(data_files_path, images_file_name)
        if not Path.is_file(file_path):
            with open(file_path, "wt", encoding="UTF-8") as file:
                json.dump({}, file, indent=4)
        with open(file_path, "rt", encoding="UTF-8") as file:
            images = json.load(file)
        return images

    def load_app_theme(self, theme_files_path: Path, theme_file_name: str) -> str:
        """load theme of application.

        Args:
            theme_files_path (Path): The path of the theme files.
            theme_file_name (str): The name of theme file.

        Returns:
            dict[str, str]: return a str that contain theme style.
        """
        file_path = Path(theme_files_path, theme_file_name)
        if not Path.is_file(file_path):
            with open(file_path, "wt", encoding="UTF-8") as file:
                file.write("")
        with open(file_path, "rt", encoding="UTF-8") as file:
            theme = file.read()
        return theme

    def find_screen_size(self) -> tuple[int, int]:
        """Find screen size in pixel.

        Returns:
            tuple[int, int]: return screen width and height.
        """
        screen_width = -1
        screen_height = -1
        for monitor in get_monitors():
            if monitor.is_primary:
                screen_width = monitor.width
                screen_height = monitor.height
                break
        return (screen_width, screen_height)

    def exec(self) -> int:
        """A method for exit the application.

        Returns:
            int: exit return code.
        """
        return self.application.exec()
