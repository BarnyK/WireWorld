from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSpinBox, QPushButton


class PositionControlWidget(QWidget):
    def __init__(self):
        super(PositionControlWidget, self).__init__()

        layout = QGridLayout(self)

        xpos_label = QLabel("X Position")
        ypos_label = QLabel("Y Position")
        self.extend_label = QLabel("Width: {:4}  Height: {:4}".format(1000, 1000))
        view_w_label = QLabel("View Width")
        view_h_label = QLabel("View Height")

        layout.addWidget(xpos_label, 0, 0, 1, 1)
        layout.addWidget(ypos_label, 0, 1, 1, 1)
        layout.addWidget(self.extend_label, 0, 2, 1, 1)
        layout.addWidget(view_w_label, 0, 3, 1, 1, Qt.AlignRight)
        layout.addWidget(view_h_label, 0, 4, 1, 1, Qt.AlignRight)

        self.xpos_spinbox = QSpinBox()
        self.ypos_spinbox = QSpinBox()
        self.extend_button = QPushButton("Extend Size")
        self.view_w_spinbox = QSpinBox()
        self.view_w_spinbox.setRange(20, 2000)
        self.view_h_spinbox = QSpinBox()
        self.view_h_spinbox.setRange(20, 2000)

        layout.addWidget(self.xpos_spinbox, 1, 0, 1, 1)
        layout.addWidget(self.ypos_spinbox, 1, 1, 1, 1)
        layout.addWidget(self.extend_button, 1, 2, 1, 1)
        layout.addWidget(self.view_w_spinbox, 1, 3, 1, 1)
        layout.addWidget(self.view_h_spinbox, 1, 4, 1, 1)

        layout.setHorizontalSpacing(20)
        self.setFixedWidth(650)

    def update_board_size(self, width, height):
        self.extend_label.setText("Width: {:4}  Height: {:4}".format(width, height))

    def set_initial_values(self, xpos, ypos, width, height):
        self.xpos_spinbox.setValue(xpos)
        self.ypos_spinbox.setValue(ypos)
        self.view_w_spinbox.setValue(width)
        self.view_h_spinbox.setValue(height)
