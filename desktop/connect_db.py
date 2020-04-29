"""
This module represents the class to work with the dialog of connecting to the database server.
"""
import json
import keyring
from os import mkdir, environ
from os.path import join, dirname, isdir, isfile
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtCore import Qt


class ConnectDatabaseDialog(QDialog):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'connect_dialog.ui')
    # Define the config directory:
    CONFIG_DIRECTORY = join(dirname(dirname(__file__)), ".config")
    # Define the config file:
    CONFIG_FILE = join(CONFIG_DIRECTORY, "config.json")

    def __init__(self, parent):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        # Initialize config directory
        self.__init_config_directory()
        # Disable resizing a window
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        # Set echo mode to hide inputting a password
        self.password_ledit.setEchoMode(QLineEdit.Password)

        self.load_config()

    def __init_config_directory(self):
        """
        This method creates directory to save all configs in here
        """
        if not isdir(self.CONFIG_DIRECTORY):
            mkdir(self.CONFIG_DIRECTORY)

    def load_config(self):
        """
        This method loads all configurations from the config file. If that file exists, then
        this method setups all configurations into the dialog.
        """
        if isfile(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as config_file:
                json_obj = json.load(config_file)
                server_names = json_obj["server_names"]
                name = json_obj["name"]
                self.remember_pswd_chebox.setChecked(json_obj["remember_pswd"])

            self.__setup_credentials(server_names, name, self.remember_pswd_chebox.isChecked())

        else:
            self.__setup_credentials()

    def __setup_credentials(self, server: list = None, name: str = "", remember_pswd: bool = False):
        """
        This method setups configurations into the dialog. It fills edit lines, combo and check boxes.
        """

        # Add all servers into server's names combobox
        if server:
            self.name_server_combox.addItems(server)

        # Set username into the user's name line edit
        self.name_user_ledit.setText(name)
        # Turn on the remembering password checkbox
        self.remember_pswd_chebox.setChecked(remember_pswd)

        # If remembering password checkbox turned on, set a password by default
        if remember_pswd:
            self.password_ledit.setText(self.__load_password_bydefault(name))

    def __save_password_bydefault(self, name: str, password: str):
        """
        This method saves the default password using the "keyring" library
        """
        keyring.set_password(environ["USERNAME"], name, password)

    def __load_password_bydefault(self, name: str):
        """
        This method loads the default password using the "keyring" library
        """
        return keyring.get_password(environ["USERNAME"], name)

    def load_credentials(self):
        pass

    def enable_connect_button(self):
        """
        This method enables or disables the connect button for this dialog window depending on whether
        there is text in the server's name combo box.
        """
        if self.name_server_combox.currentText():
            self.connect_button.setEnabled(True)
        else:
            self.connect_button.setEnabled(False)