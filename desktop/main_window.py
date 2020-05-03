"""
This module represents the class to work with the main window.
"""
from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from desktop.connect_db import ConnectDatabaseDialog
from desktop.central_widget import CentralWidget


class MainWindow(QMainWindow):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'main_window.ui')

    def __init__(self):
        super().__init__()

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        self.connect_db_dialog = None
        self.connection = None

        self.connect_db()

    def connect_db(self):
        """
        This function creates the connect database dialog and settings it
        """
        self.connect_db_dialog = ConnectDatabaseDialog(self)
        self.connect_db_dialog.show()

    def set_connection(self, connection):
        """
        When connection will be established in the dialog window, then this method will be called
        and the connection will be passed in here.
        """
        self.connection = connection

        self.connect_action.setEnabled(False)
        self.disconnect_action.setEnabled(True)

        central_widget = CentralWidget(self, self.connection)
        self.setCentralWidget(central_widget)

    def disconnect_db(self):
        """
        This method will close all tables and a database
        """
        if self.connection:
            self.connection = None

        self.disconnect_action.setEnabled(False)
        self.connect_action.setEnabled(True)

        self.centralWidget().deleteLater()
        self.setCentralWidget(None)
