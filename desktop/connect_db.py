"""
This module represents the class to work with the dialog of connecting to the database server.
"""
from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt


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

        # Disable resizing a window
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.load_credentials()

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