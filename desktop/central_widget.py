from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget
from desktop.table_widget import TableWidget
from desktop.logs_dialog import GetLogsDialog


class CentralWidget(QWidget):
    # Define the directory of ui's files
    UI_DIR = join(dirname(__file__), 'resources', 'ui')
    # Define the filename to ui file of that widget
    FILENAME_UI = join(UI_DIR, 'central_widget.ui')

    def __init__(self, parent, database):
        super().__init__(parent)

        # Load .ui file and initialize it
        try:
            uic.loadUi(self.FILENAME_UI, self)
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        self.database = database
        self.setup_tables()

    def setup_tables(self):
        """
        This method setups all tables into central widget
        """
        # Set new tables into tab widget
        for table_name in self.database.get_tables():
            widget = self.create_table(table_name)
            self.tab_widget.addTab(widget, table_name)

    def create_table(self, table_name: str, widget: QWidget = None) -> QWidget:
        """
        This method creates new table widget, sets all configurations and returns created widget
        """
        if widget is None:
            widget = QWidget()
        table_widget = TableWidget(widget, self.database, table_name, auto_update=True)
        layout = QGridLayout()
        layout.addWidget(table_widget)
        widget.setLayout(layout)

        return widget

    def delete_tuple(self):
        """
        This is a slot which will be called when the delete button will be clicked
        """
        # Determine the table name, then find the table and call its delete method
        table_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        widget = self.tab_widget.currentWidget()
        if widget:
            table = widget.findChild(QTableWidget, table_name)
            if table:
                table.delete_tuple()

            self.update_tables()

    def create_deleting_dialog(self, columns, rows):
        pass

    def update_tables(self):
        """
        This method makes an value update of all tables
        """
        for tab_index in range(self.tab_widget.count()):
            table_name = self.tab_widget.tabText(tab_index)
            widget = self.tab_widget.widget(tab_index)
            table = widget.findChild(QTableWidget, table_name)
            table.update_table()

    def get_logs_dialog(self):
        """
        Get the Dialog and set the values in this table.
        """
        table_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        dialog = GetLogsDialog(self, self.database, table_name)
        dialog.show()

        widget = self.tab_widget.currentWidget()
        if widget:
            table = widget.findChild(QTableWidget, table_name)
            if table:
                rows = table.get_rows(selected=True)
                dialog.set_values(rows)