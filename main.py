from PyQt5.QtWidgets import QApplication

import sys

import main_ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_ui.MainWindow()
    window.show()
    app.exec_()

