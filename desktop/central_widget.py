from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGridLayout
from desktop.table_widget import TableWidget


class CentralWidget(QWidget):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'central_widget.ui')

    def __init__(self, parent, connection):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        self.connection = connection

        self.setup_tables()

    def setup_tables(self):
        """
        This method setups all tables into central widget
        """
        cursor = self.connection.cursor()

        # Get all names of the tables containing in the database, except of the diagrams system table
        tables = cursor.execute("""
        SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME <> 'sysdiagrams'
        """).fetchall()
        tables = [table[0] for table in tables]

        # Set new tables into tab widget
        for table_name in tables:
            widget = self.create_table(table_name)
            self.tab_widget.addTab(widget, table_name)

    def create_table(self, table_name) -> QWidget:
        """
        This method creates new table widget, sets all configurations and returns created widget
        """
        widget = QWidget()
        table_widget = TableWidget(widget)
        layout = QGridLayout()
        layout.addWidget(table_widget)
        widget.setObjectName(table_name)
        widget.setLayout(layout)

        return widget
