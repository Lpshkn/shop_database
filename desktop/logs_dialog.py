"""
Module for the getting logs dialog. This module gets logs from the CDC tables of the database
and print it into the table in the dialog.
"""

from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from desktop.database import Database
from desktop.table_widget import TableWidget


class GetLogsDialog(QDialog):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'get_logs_dialog.ui')

    def __init__(self, parent, database: Database, table_name: str):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        # Set settings of the window
        self.setWindowTitle(f"Журнал действий таблицы {table_name}")
        self.setWindowFlags(Qt.Dialog)

        self.database = database
        self.table_name = table_name

        # Create the table widget and add it to the layout
        self.table_widget = TableWidget(self, self.database, table_name)
        self.layout.insertWidget(0, self.table_widget)

        # Set the names of columns
        columns = ['Действие']
        columns.extend(self.database.get_columns(table_name))
        self.table_widget.set_columns(columns)

    def set_values(self, rows: list):
        """
        Method sets values in the table.

        :param rows: the values that will be set
        """
        # Get the name of columns
        columns = self.database.get_columns(self.table_name)
        # The name of the CDC table
        table_name = f"{self.database.default_schema}_{self.table_name}_CT"

        _rows = []
        for row in rows:
            self.database.add_query(f"""
                SELECT __$operation, {', '.join(columns)}
                FROM cdc.{table_name}
                WHERE {columns[0]} = {row[0]}
                """)
            for it in self.database.execute_query().fetchall():
                if it[0] == 2:
                    _rows.append(["Добавление"] + list(it[1:]))
                elif it[0] == 3:
                    _rows.append(["Значение до изменения"] + list(it[1:]))
                elif it[0] == 4:
                    _rows.append(["Значение после изменения"] + list(it[1:]))

        self.table_widget.set_rows(_rows, flags=(Qt.ItemIsSelectable, Qt.ItemIsEnabled))