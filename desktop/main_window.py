"""
This module represents the class to work with the main window.
"""
from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from desktop.connect_db import ConnectDatabaseDialog


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

        self.connect_db()

    def create_db_dialog(self):
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
