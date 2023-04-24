import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, qRgb
from game import Game
from PyQt5.QtCore import Qt


def create_tool_selector(game: Game):
    possible_values = game.possible_values()
    tool_selector = QComboBox()
    for name, value in possible_values:
        tool_selector.addItem(name, value)

    label = QLabel("Tool:")
    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(tool_selector)
    return tool_selector, layout


class GameBoardUI(QWidget):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.xpos = 0
        self.ypos = 0
        self.width = 10
        self.height = 20
        # Ensure board dimensions here
        self.tool = 0
        self.color_table = [qRgb(*t) for t in self.game.color_table()]

        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setScaledContents(True)
        self.image_display.setMinimumSize(640, 400)
        self.image_display.mousePressEvent = self.image_press_event

        # EDIT UI
        self.tool_selector, tool_layout = create_tool_selector(self.game)

        edit_layout = QHBoxLayout()
        edit_layout.addLayout(tool_layout)

        # tool selector, expand, move

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_display)
        self.main_layout.addLayout(edit_layout)
        self.setLayout(self.main_layout)

        self.update_board()

    def update_board(self):
        board = self.game.get_board(self.xpos, self.ypos, self.width, self.height, pad=True)

        image = QImage(board.data, board.shape[1], board.shape[0], board.strides[0], QImage.Format_Indexed8)
        image.setColorTable(self.color_table)
        pixmap = QPixmap(image)
        self.image_display.setPixmap(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation))

    def next_frame(self):
        self.game.next()

    def image_press_event(self, event):
        print("MousePressEvent")

        label_size = self.image_display.size()
        pixmap_size = self.image_display.pixmap().size()
        # print(label_size, pixmap_size)
        # width_offset = (label_size.width() - pixmap_size.width()) / 2
        # height_offset = (label_size.width() - pixmap_size.width()) / 2

        # print(width_offset, height_offset)
        # print(width_offset, height_offset)
        x = event.pos().x() #- width_offset
        y = event.pos().y() #- height_offset
        print(event.pos().x(), x)

        size = self.image_display.size()
        pixels_per_point_w = size.width() / self.width
        pixels_per_point_h = size.height() / self.height

        board_x = int(x // pixels_per_point_w + self.xpos)
        board_y = int(y // pixels_per_point_h + self.ypos)

        # print(x,y)
        # print(board_x,board_y)
        # print(f"{x / pixels_per_point_w}, {y / pixels_per_point_h}")

        # board_x = int(x * self.width / self.image_display.pixmap().width())
        # board_y = int(x * self.height / self.image_display.pixmap().height())

        if event.button() == Qt.RightButton:
            tool_value = 0
        else:
            tool_value = self.tool_selector.currentData(Qt.UserRole)

        self.game.set(board_x, board_y, tool_value)
        self.update_board()

    def ensure_game_size(self):
        h, w = self.game.get_board_size()
        extend_h = max(self.height - h, 0)
        extend_w = max(self.width - w, 0)
        if extend_w >0 or extend_h > 0:
            self.game.expand_board(0,0,extend_h,extend_w)

    def move_board(self, xdiff, ydiff):
        pass




