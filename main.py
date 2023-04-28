import sys

from PyQt5.QtWidgets import QApplication

import main_ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_ui.MainWindow()
    #window.setStyleSheet("border: 1px solid blue;")
    window.show()
    app.exec_()
