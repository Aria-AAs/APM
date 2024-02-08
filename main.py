"""Main module of the application
Run this to start the application
"""

from sys import argv
from sys import exit as ex
from src.application import Application


if __name__ == "__main__":
    ex(Application(argv).exec())
