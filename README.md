# APM

A password manager application which is written in Python using PyQt6 by Aria-AAs

![Static Badge](https://img.shields.io/badge/Author-Aria--AAs-orange?style=plastic&link=https%3A%2F%2Fgithub.com%2FAria-AAs)
[![Static Badge](https://img.shields.io/badge/build-GPL%20V3-brightgreen?style=plastic&label=Licence&link=https%3A%2F%2Fgithub.com%2FAriaAs5%2Fpassword_manager%2Fblob%2Fmain%2FLICENSE)](https://img.shields.io/badge/License-GPL_V3-brightgreen?style=plastic&link=https%3A%2F%2Fgithub.com%2FAria-AAs%2FAPM%2Fblob%2Fmain%2FLICENSE)
[![Static Badge](https://img.shields.io/badge/build-Python-blue?style=plastic&label=Language&link=https%3A%2F%2Fgithub.com%2FAriaAs5%2Fpassword_manager%2Fblob%2Fmain%2FLICENSE)](https://img.shields.io/badge/Language-Python-blue?style=plastic&link=https%3A%2F%2Fwww.python.org%2F)
![Static Badge](https://img.shields.io/badge/Lines_of_code-%2B3K-purple?style=plastic)

## Please be cautious.

The application is in the beta version.

**Not encrypted yet.**

## What APM is?
APM stands for **Aria-AAs password manager**. It is a simple and minimal password manager

It allows you to securely save usernames and passwords under different names with a simple GUI interface.

## How to use APM?

Some important notes.
- **Note:** The application is in beta version. so it may not be safe enough yet.
- **Note:** As the application does not have auto-updater yet, you should check this page continuously to update the application manually.
- **Note:** The application tested only on Windows.

- [Windows](#windows)
- [Linux](#linux)

#### Windows:

1. Download the zip file of the repository.
2. Extract the downloaded file.
3. Make sure that Python is installed on your system.
4. Open a command prompt.
5. Go to the root folder of the project.
6. Run `pip install -r requirements.txt`
7. Run `python main.py`
8. Enjoy.

#### Linux:

1. Make sure that version 3 of Python is installed on your system.
2. Open a terminal.
3. Run `sudo apt install xsel xclip`
4. Run `git clone https://github.com/Aria-AAs/APM.git`
5. Go to the APM directory.
6. Make a virtual environment.
    - We recommend you use the virtualenv to do this task.
        1. Install it using `pip install virtualenv`
        2. Make a new virtual environment using `virtualenv venv`
7. Active the virtual environment that you made in the previous step.
    - if you are using virtualenv you can active it using `source venv/bin/activate`
8.  Run `pip install -r requirements.txt`
9.  Run `python3 main.py`
10. Enjoy.

## TODO:

- [x] - Secure the main password with hashing and salting
- [x] - Secure the secrets with AES.CBC encryption
- [x] - Regenerate the hash of the main password after each login
- [x] - Make a password generator
- [x] - Add some theme to the application
- [x] - Add dark mode to the application
- [x] - Add reset factory to the application
- [ ] - Make auto-updater
- [ ] - Make sure that the application keeps secrets safe
- [ ] - Fix not scrolling the content area