from PyQt5.QtWidgets import QMainWindow, QPushButton, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QSpinBox

import game
from game_board_ui import GameBoardUI


def make_speed_selector():
    speed_selector = QDoubleSpinBox()
    speed_selector.setRange(0,50)
    speed_selector.setSingleStep(0.1)
    label = QLabel("Frames Per Second")
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(speed_selector)
    return speed_selector, layout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "WireWorld Simulator"
        self.setWindowTitle(self.title)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Control UI elements
        self.play_button = QPushButton("Start")
        self.next_frame_button = QPushButton("Next")
        self.speed_selector, self.speed_selector_layout = make_speed_selector()

        # Game board
        init_game = game.WireWorld()
        self.game_holder = GameBoardUI(init_game)

        # Control UI elements functionality
        self.playing = False
        self.play_button.clicked.connect(self.play)

        self.next_frame_button.clicked.connect(self.next_frame)

        self.fps = 1
        self.speed_selector.setValue(self.fps)
        self.speed_selector.valueChanged.connect(self.fps_change)

        # Control layout
        control_layout = QHBoxLayout()
        control_layout.addLayout(self.speed_selector_layout)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.next_frame_button)

        self.main_layout = QVBoxLayout()
        # GAME UI
        self.main_layout.addWidget(self.game_holder)
        # EDIT UI
        # CONTROL UI
        self.main_layout.addLayout(control_layout)
        self.main_widget.setLayout(self.main_layout)

    def next_frame(self):
        print("Next frame clicked")
        self.game_holder.next_frame()
        self.game_holder.update_board()

    def play(self):
        print("Play button clicked")
        time_delimeter = self.fps * 1000
        self.game_holder.play(time_delimeter)

    def fps_change(self,v: float):
        self.fps = v
        print(f"fps changed to {v}")

    def load_file(self):
        pass

    def save_file(self):
        pass









