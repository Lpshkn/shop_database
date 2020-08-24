"""
Module for the adding values dialog. This module processes the dialog that adds new values.
"""
import desktop.database as db
from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt


class AddingValuesDialog(QDialog):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'adding_values_dialog.ui')

    def __init__(self, parent, database: db.Database, table_name: str):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        # Set settings of the window
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.database = database
        self.table_name = table_name
        self._initialize()

    def _initialize(self):
        """
        Method sets fields in the dialog.
        """
        # Set the table name above the other edit lines
        self.table_name_label.setText(db.TABLES[self.table_name])

        # Get the name of columns. Don't use the first column because of it's IDENTITY and won't be set by user.
        columns = self.database.get_columns(self.table_name)[1:]
        for index, column in enumerate(columns):
            label = QLabel(db.COLUMNS[column], self)
            font = label.font()
            font.setPointSize(9)
            label.setFont(font)
            self.main_layout.addWidget(label, index, 0)

            ledit = QLineEdit(self)
            ledit.setFont(font)
            self.main_layout.addWidget(ledit, index, 1)
