from os.path import join, dirname
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


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
