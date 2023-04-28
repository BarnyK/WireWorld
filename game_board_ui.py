from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QHBoxLayout, QSpinBox, QPushButton

import extend_board_dialog
from game import Game


def make_tool_selector(game: Game):
    possible_values = game.possible_values()
    tool_selector = QComboBox()
    for name, value in possible_values:
        tool_selector.addItem(name, value)

    label = QLabel("Tool:")
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(tool_selector)
    return tool_selector, layout


def make_labeled_spinbox(label_name, slot, min_value, max_value, initial_value):
    label = QLabel(label_name)
    label.setAlignment(Qt.AlignCenter)

    spin = QSpinBox()
    spin.setRange(min_value, max_value)
    spin.setValue(initial_value)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(spin)
    spin.valueChanged.connect(slot)

    spin.setFixedWidth(90)
    label.setFixedWidth(90)
    # layout.setAlignment(Qt.AlignCenter)
    layout.setContentsMargins(5, 0, 5, 0)
    layout.setSpacing(0)
    return spin, layout


def make_help_information():
    content = QLabel("Left click to place cell\nRight click to empty cell")
    return content

def make_extend_board_widget(width, height):
    width_label = QLabel(f"Width {width}\tHeight: {height}")
    button = QPushButton("Extend Size")

    w = QWidget()
    layout = QVBoxLayout(w)
    layout.addWidget(width_label)
    layout.addWidget(button)
    layout.setSpacing(0)

    return w



class GameBoardUI(QWidget):
    def __init__(self, game: Game):
        super().__init__()
        self.state = "paused"
        self.game = game
        self.xpos = 0
        self.ypos = 0
        self.width = 30
        self.height = 40

        self.color_table = [qRgb(*t) for t in self.game.color_table()]

        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setScaledContents(True)
        self.image_display.setMinimumSize(600, 400)
        self.image_display.mousePressEvent = self.image_press_event

        # EDIT UI
        self.tool_selector, tool_layout = make_tool_selector(self.game)
        help_information = make_help_information()

        # Position and size control
        self.xpos_spinbox, xpos_spinbox_layout = make_labeled_spinbox("X Position", self.move_board_x, 0,
                                                                      self.board_width() - self.width, self.xpos)
        self.ypos_spinbox, ypos_spinbox_layout = make_labeled_spinbox("Y Position", self.move_board_y, 0,
                                                                      self.board_height() - self.height, self.ypos)
        self.width_spinbox, width_spinbox_layout = make_labeled_spinbox("View Width", self.change_view_width, 15, 2000,
                                                                        self.width)
        self.height_spinbox, height_spinbox_layout = make_labeled_spinbox("View Height", self.change_view_height, 20,
                                                                          2000,
                                                                          self.height)

        self.extend_board_widget = extend_board_dialog.ExtendBoardWidget(self.board_width(), self.board_height())
        # Setup of position and size control widget
        pas = QWidget()
        pas_layout = QHBoxLayout()

        for spin in [xpos_spinbox_layout, ypos_spinbox_layout]:
            pas_layout.addLayout(spin)

        pas_layout.addStretch()
        pas_layout.addWidget(self.extend_board_widget)
        pas_layout.addStretch()
        for spin in [width_spinbox_layout, height_spinbox_layout]:
            pas_layout.addLayout(spin)

        pas.setFixedWidth(600)
        pas_layout.setAlignment(Qt.AlignCenter)
        pas.setLayout(pas_layout)

        # Setup of edit widget
        edit_widget = QWidget()
        edit_layout = QHBoxLayout()
        edit_layout.addLayout(tool_layout)
        edit_layout.addStretch()
        edit_layout.addWidget(help_information)

        edit_widget.setFixedWidth(600)
        edit_widget.setLayout(edit_layout)
        edit_widget.setContentsMargins(25, 0, 25, 0)

        # Setup of main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(pas, 0, Qt.AlignCenter)
        self.main_layout.addWidget(self.image_display)
        self.main_layout.addWidget(edit_widget, 0, Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.ensure_game_size()
        self.update_board()

    def update_board(self):
        print("update_board")
        board = self.game.get_board(self.xpos, self.ypos, self.width, self.height, pad=True)

        image = QImage(board.data, board.shape[1], board.shape[0], board.strides[0], QImage.Format_Indexed8)
        image.setColorTable(self.color_table)
        pixmap = QPixmap(image)
        self.image_display.setPixmap(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def next_frame(self):
        self.game.next()
        self.update_board()

    def play(self, time_delimiter: int):
        if self.state == "playing":
            self._pause()
        elif self.state == "paused":
            self._play(time_delimiter)

    def _play(self, time_delimeter: int):
        print("Play")
        self.state = "playing"
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(time_delimeter)

    def _pause(self):
        print("Pause")
        self.state = "paused"
        self.timer.stop()

    def image_press_event(self, event):
        print("MousePressEvent")

        x = event.pos().x()
        y = event.pos().y()

        size = self.image_display.size()
        pixels_per_point_w = size.width() / self.width
        pixels_per_point_h = size.height() / self.height

        board_x = int(x // pixels_per_point_w + self.xpos)
        board_y = int(y // pixels_per_point_h + self.ypos)

        if event.button() == Qt.RightButton:
            tool_value = 0
        else:
            tool_value = self.tool_selector.currentData(Qt.UserRole)

        self.game.set(board_x, board_y, tool_value)
        self.update_board()

    def ensure_game_size(self):
        w, h = self.game.get_board_size()
        extend_h = max(self.height - h + self.ypos, 0)
        extend_w = max(self.width - w + self.xpos, 0)
        if extend_w > 0 or extend_h > 0:
            self.game.expand_board(0, extend_w, 0, extend_h)
            self.update_position_spinbox_ranges()

    def change_view_width(self, value):
        self.width = value
        self.ensure_game_size()
        self.update_position_spinbox_ranges()
        self.update_board()

    def change_view_height(self, value):
        self.height = value
        self.ensure_game_size()
        self.update_position_spinbox_ranges()
        self.update_board()

    def move_board_x(self, value):
        width = self.board_width()
        self.xpos = min(value, width - self.width)
        self.update_board()

    def move_board_y(self, value):
        height = self.board_height()
        self.ypos = min(value, height - self.height)
        self.update_board()

    def board_width(self) -> int:
        width, _ = self.game.get_board_size()
        return width

    def board_height(self) -> int:
        _, height = self.game.get_board_size()
        return height

    def resizeEvent(self, a0) -> None:
        self.update_board()

    def update_position_spinbox_ranges(self):
        self.xpos_spinbox.setRange(0, self.board_width() - self.width)
        self.ypos_spinbox.setRange(0, self.board_height() - self.height)

    def load_game_file(self, filepath: str):
        self.game.load_board(filepath)
        self.xpos = 0
        self.ypos = 0
        self.ensure_game_size()
        self.update_board()

    def save_game_file(self, filepath: str):
        self.game.save_board(filepath)

    def open_extend_board_dialog(self):
        dialog = extend_board_dialog.Dialog(self)
        dialog.setModal(True)
        dialog.valuesSubmited.connect(self.extend_board_slot)
        dialog.exec_()

    def extend_board_slot(self, x1: int, x2: int, y1: int, y2: int):
        print(x1, x2, y1, y2)
        # self.game.expand_board(x1, x2, y1, y2)
