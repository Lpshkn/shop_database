"""
This module represents the class to work with the dialog of connecting to the database server.
"""
from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class ConnectDatabaseDialog(QDialog):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'connect_dialog.ui')

    def __init__(self, parent):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        self.load_logs()

    def load_logs(self):
        pass
