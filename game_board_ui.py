from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QHBoxLayout, QSpinBox

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
    spin = QSpinBox()
    spin.setRange(min_value, max_value)
    spin.setValue(initial_value)
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(spin)
    spin.valueChanged.connect(slot)
    return spin, layout


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
        self.image_display.setMinimumSize(640, 400)
        self.image_display.mousePressEvent = self.image_press_event

        # EDIT UI
        self.tool_selector, tool_layout = make_tool_selector(self.game)

        # Position and size control
        self.xpos_spinbox, xpos_spinbox_layout = make_labeled_spinbox("XPOS", self.move_board_x, 0,
                                                                      self.board_width() - self.width, self.xpos)
        self.ypos_spinbox, ypos_spinbox_layout = make_labeled_spinbox("YPOS", self.move_board_y, 0,
                                                                      self.board_height() - self.height, self.ypos)
        self.width_spinbox, width_spinbox_layout = make_labeled_spinbox("Width", self.change_view_width, 15, 2000,
                                                                        self.width)
        self.height_spinbox, height_spinbox_layout = make_labeled_spinbox("Height", self.change_view_height, 20, 2000,
                                                                          self.height)

        pas_layout = QHBoxLayout()
        for spin in [xpos_spinbox_layout, ypos_spinbox_layout, width_spinbox_layout, height_spinbox_layout]:
            pas_layout.addLayout(spin)

        edit_layout = QHBoxLayout()
        edit_layout.addLayout(tool_layout)

        # tool selector, expand, move

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(pas_layout)
        self.main_layout.addWidget(self.image_display)
        self.main_layout.addLayout(edit_layout)
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

    def play(self, time):
        if self.state == "playing":
            self._pause()
        if self.state == "paused":
            self._play()

    def _play(self):
        self.state = "paused"
        pass

    def _pause(self):
        self.state = "playing"
        pass

    def image_press_event(self, event):
        print("MousePressEvent")

        x = event.pos().x()  # - width_offset
        y = event.pos().y()  # - height_offset

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
