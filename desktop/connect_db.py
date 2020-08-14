"""
This module represents the class to work with the dialog of connecting to the database server.
"""
import json
import keyring
import pyodbc
import re
from os import mkdir, environ
from os.path import join, dirname, isdir, isfile
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFrame, QFormLayout
from PyQt5.QtCore import Qt
from desktop.convert_error_sql import convert_error_sql
from desktop.database import Database


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

        # Flag specifies that Windows credential will be used
        self.trusted_connection = 'yes'
        # Define error label to print error message it the dialog
        self.error_label = None
        self.error_line = None
        # Initialize config directory
        self.__init_config_directory()
        # Disable resizing a window
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        # Set echo mode to hide inputting a password
        self.password_ledit.setEchoMode(QLineEdit.Password)

        self.database = None

        self.__load_config()

    def __init_config_directory(self):
        """
        This method creates directory to save all configs in here
        """
        if not isdir(self.CONFIG_DIRECTORY):
            mkdir(self.CONFIG_DIRECTORY)

    def __load_config(self):
        """
        This method loads all configurations from the config file. If that file exists, then
        this method setups all configurations into the dialog.
        """
        if isfile(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as config_file:
                json_obj = json.load(config_file)
                server_names = json_obj["server_names"]
                database_names = json_obj["database_names"]
                name = json_obj["name"]
                self.remember_pswd_chebox.setChecked(json_obj["remember_pswd"])

            self.__setup_credentials(server_names, database_names, name, self.remember_pswd_chebox.isChecked())

        else:
            self.__setup_credentials()

    def __setup_credentials(self, server: list = None, database: list = None, name: str = "", remember_pswd: bool = False):
        """
        This method setups configurations into the dialog. It fills edit lines, combo and check boxes.
        """

        # Add all servers and databases into server's names combobox and database's names combobox
        if server:
            self.name_server_combox.addItems(server)
        if database:
            self.database_combox.addItems(database)

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

    def __save_config(self):
        config = dict()

        # Get all names of servers and serialize it
        config["server_names"] = [self.name_server_combox.itemText(i) for i in range(self.name_server_combox.count())]
        current_server = self.name_server_combox.currentText()
        if current_server not in config["server_names"]:
            config["server_names"].append(current_server)

        # Get all names of databases and serialize it
        config["database_names"] = [self.database_combox.itemText(i) for i in range(self.database_combox.count())]
        current_database = self.database_combox.currentText()
        if current_database not in config["database_names"]:
            config["database_names"].append(current_database)

        config["name"] = self.name_user_ledit.text()
        config["remember_pswd"] = self.remember_pswd_chebox.isChecked()

        # If it's true, save the password using keyring
        if config["remember_pswd"]:
            self.__save_password_bydefault(name=self.name_user_ledit.text(), password=self.password_ledit.text())

        with open(self.CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file)

    def enable_connect_button(self):
        """
        This method enables or disables the connect button for this dialog window depending on whether
        there is text in the server's name combo box.
        """
        if self.name_server_combox.currentText() and self.database_combox.currentText():
            self.connect_button.setEnabled(True)
        else:
            self.connect_button.setEnabled(False)

    def connect(self):
        """
        This methods gets all values from window's fields and passes them into connecting to database method
        """

        server = self.name_server_combox.currentText()
        database = self.database_combox.currentText()
        name = self.name_user_ledit.text()
        password = self.password_ledit.text()

        try:
            # Take connection to a database
            self.database = Database.connect_db(server, database, name, password, autocommit=True,
                                                trusted_connection=self.trusted_connection)
        except (pyodbc.InterfaceError, pyodbc.OperationalError) as e:
            self.set_error_connection(e.args)
            return

        # Close dialog window
        self.reject()

        # If the connection was established, then save all configurations into the configuration file
        self.__save_config()
        # Pass established connection into main window class
        self.parent().set_connection(self.database.connection)

    def set_error_connection(self, error):
        """
        This method sets error label if error has been occurred
        """
        if not self.error_line:
            self.error_line = QFrame(self)
            self.error_line.setFrameShadow(QFrame.Sunken)
            self.error_line.setFrameShape(QFrame.HLine)
            self.error_line.setLineWidth(1)
            self.fields_layout.insertWidget(1, self.error_line)

        if not self.error_label:
            error_msg = convert_error_sql(error)

            self.error_label = QLabel(error_msg, self)
            self.error_label.setWordWrap(True)
            self.error_label.setStyleSheet('QLabel { color : red; }')
            self.fields_layout.insertWidget(2, self.error_label)

            self.resize(self.sizeHint())

    def remove_error_connection(self):
        """
        This method is slot which called when any field was edited. If error label and line are set,
        then this method remove these widgets
        """
        if self.error_line:
            self.fields_layout.removeWidget(self.error_line)
            self.error_line.deleteLater()
            self.error_line = None

        if self.error_label:
            self.fields_layout.removeWidget(self.error_label)
            self.error_label.deleteLater()
            self.error_label = None

            self.resize(self.sizeHint())

    def enable_login_pswd(self):
        flag = False
        self.trusted_connection = 'yes'

        if self.autentification_combox.currentText() == 'Логин и пароль':
            flag = True
            self.trusted_connection = 'no'

        for i in range(self.credentials_formlayout.count()):
            obj = self.credentials_formlayout.itemAt(i).widget()
            obj.setEnabled(flag)
