from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, \
    QFileDialog, QDialog, QFrame

import game
from game_board_ui import GameBoardUI


def make_speed_selector():
    speed_selector = QDoubleSpinBox()
    speed_selector.setRange(0, 100)
    speed_selector.setSingleStep(0.1)
    label = QLabel("Frames Per Second")
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(speed_selector)
    return speed_selector, layout


class MainWindow(QMainWindow):
    """
        MainWindows holds controls, game board, and file handling UI
    """
    def __init__(self):
        super().__init__()
        self.title = "WireWorld Simulator"
        self.setWindowTitle(self.title)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)

        # Control UI elements
        self.play_button = QPushButton("Play")
        self.next_frame_button = QPushButton("Next Frame")
        self.speed_selector, self.speed_selector_layout = make_speed_selector()

        # Game board
        init_game = game.WireWorld()
        self.game_holder = GameBoardUI(init_game)

        # Control UI elements functionality
        self.playing = False
        self.play_button.clicked.connect(self.play)

        self.next_frame_button.clicked.connect(self.next_frame)

        self.fps = 15
        self.speed_selector.setValue(self.fps)
        self.speed_selector.valueChanged.connect(self.fps_change)

        # Control layout
        control = QWidget()
        control_layout = QHBoxLayout()
        control_layout.addLayout(self.speed_selector_layout)
        control_layout.addWidget(self.next_frame_button)
        control_layout.addWidget(self.play_button)

        control.setFixedWidth(600)
        control.setLayout(control_layout)

        # File buttons
        file_buttons = QWidget()
        file_buttons_layout = self.make_save_load_buttons()
        file_buttons.setFixedWidth(650)
        file_buttons.setLayout(file_buttons_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedWidth(650)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFixedWidth(650)

        # Setup of main layout
        self.main_layout = QVBoxLayout()
        # Saving a loading buttons
        self.main_layout.addWidget(file_buttons, 0, Qt.AlignCenter)
        self.main_layout.addWidget(line, 0, Qt.AlignCenter)
        # GAME UI
        self.main_layout.addWidget(self.game_holder, 2, Qt.AlignCenter)
        # CONTROL UI
        self.main_layout.addWidget(line2, 0, Qt.AlignCenter)
        self.main_layout.addWidget(control, 0, Qt.AlignCenter)
        self.main_widget.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)

    def next_frame(self):
        self.game_holder.next_frame()

    def play(self):
        time_delimiter = int(1 / self.fps * 1000)
        self.game_holder.play(time_delimiter)

        if self.game_holder.state == "paused":
            self.play_button.setText("Play")
        elif self.game_holder.state == "playing":
            self.play_button.setText("Pause")

    def make_save_load_buttons(self):
        save = QPushButton("Save")
        save.clicked.connect(self.save_file)

        load = QPushButton("Load")
        load.clicked.connect(self.load_file)

        layout = QHBoxLayout()
        layout.addWidget(save)
        layout.addWidget(load)
        return layout

    def fps_change(self, v: float):
        self.fps = v

    def load_file(self):
        dialog = QDialog()
        dialog.setModal(True)
        filename, _ = QFileDialog.getOpenFileName(dialog, 'Load file', '', 'Numpy File(*.npy)')
        if filename:
            self.game_holder.load_game_file(filename)

    def save_file(self):
        dialog = QDialog()
        dialog.setModal(True)
        filename, _ = QFileDialog.getSaveFileName(dialog, 'Save file', '', 'Numpy File(*.npy)')
        if filename:
            self.game_holder.save_game_file(filename)
