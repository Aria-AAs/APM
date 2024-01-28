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

## How to use APM.

Some important notes.
- **Note:** The application is in beta version. so it may not be safe enough yet.
- **Note:** As the application does not have auto-updater yet, you should check this page continuously to update the application manually.
- **Note:** As the application has no release, the only option to use it is the developer mode.

### Install in developer mode:

- [Windows](#windows)
- [Linux](#linux)

#### Windows:

- Download the zip file of the repository.
- Extract the downloaded file.
- Make sure that Python is installed on your system.
- Open a command prompt.
- Go to the root folder of the project.
- Run `pip install -r requirements.txt`
- Run `python main.py`
- Enjoy.

#### Linux:

- Make sure that Python version 3 is installed on your system.
- Open a terminal.
- Go to the root directory of the project.
- Run `git clone https://github.com/Aria-AAs/APM.git`
- Run `pip3 install -r requirements.txt`
- Run `python3 main.py`
- Enjoy.

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