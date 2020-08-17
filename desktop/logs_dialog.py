"""
Module for the getting logs dialog. This module gets logs from the CDC tables of the database
and print it into the table in the dialog.
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


class GetLogsDialog(QDialog):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'get_logs_dialog.ui')

    def __init__(self, parent, database):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self.database = database
