from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QFormLayout, QSpinBox, QPushButton


class Dialog(QDialog):
    valuesSubmited = pyqtSignal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extend Board")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setFixedSize(200, 170)

        layout = QFormLayout(self)

        self.left_spinbox = QSpinBox()
        layout.addRow(f"Left", self.left_spinbox)

        self.right_spinbox = QSpinBox()
        layout.addRow(f"Right", self.right_spinbox)

        self.top_spinbox = QSpinBox()
        layout.addRow(f"Top", self.top_spinbox)

        self.bottom_spinbox = QSpinBox()
        layout.addRow(f"Bottom", self.bottom_spinbox)

        for spinbox in [self.left_spinbox, self.right_spinbox, self.top_spinbox, self.bottom_spinbox]:
            spinbox.setRange(0, 1000)

        button = QPushButton("Submit")
        button.clicked.connect(self.submit)
        layout.addRow(button)

    def submit(self):
        result = []
        for spinbox in [self.left_spinbox, self.right_spinbox, self.top_spinbox, self.bottom_spinbox]:
            result.append(spinbox.value())
        self.valuesSubmited.emit(*result)
        self.accept()


if __name__ == "__main__":
    app = QApplication([])
    dialog = Dialog()
    dialog.valuesSubmited.connect(lambda a, b, c, d: print(a, b, c, d))
    dialog.exec_()
