import numpy as np

import neighbourhood


class Game:
    """Game is a class implementing the operation of the cellular automata"""

    def __init__(self):
        pass

    def add(self, x: int, y: int) -> None:
        """
            Add updates board by iterating to next value of state
        :param x: horizontal coordinate of the board
        :param y: vertical coordinate of the board
        """
        pass

    def set(self, x: int, y: int, v: int) -> None:
        """
            Set updates the board position x, y with value v
        :param x: horizontal coordinate of the board
        :param y: vertical coordinate of the board
        :param v: value to put in place
        """
        pass

    def next(self) -> None:
        """
            Next updates the game to the new state
        """
        pass

    def get_board(self, x: int, y: int, width: int = -1, height: int = -1, pad: bool = False) -> np.ndarray:
        """
            get_board returns part of the board as numpy.ndarray
        :param x: horizontal element of the top left element to return
        :param y: vertical element of the top left element to return
        :param width: width of the returned board
        :param height: height of the returned board
        :param pad: whether the resulting array should be padded
        :return:
        """
        pass

    def expand_board(self, x1: int, x2: int, y1: int, y2: int) -> None:
        """
            expand_board expands the board in 4 direction
        :param x1: expansion to the left
        :param x2: expansion to the right
        :param y1: expansion to the top
        :param y2: expansion to the bottom
        """
        pass

    @staticmethod
    def get_color_dict() -> dict:
        pass

    @staticmethod
    def color_table() -> list:
        pass

    @staticmethod
    def possible_values() -> list:
        pass

    def get_board_size(self) -> tuple:
        pass

    def load_board(self, filename: str):
        pass

    def save_board(self, filename: str):
        pass


DEFAULT_BOARD_SIZE = (100, 100)
EMPTY = 0
ELECTRON_HEAD = 1
ELECTRON_TAIL = 2
CONDUCTOR = 3


class WireWorld(Game):
    def __init__(self, board: np.ndarray = None):
        super(Game).__init__()
        if board is None:
            self.board = np.array(
                [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 3, 0, 0], [0, 3, 0, 0, 0, 3, 0], [0, 0, 3, 3, 3, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]], dtype=np.int8)
        else:
            self.board = board

    def add(self, x: int, y: int) -> None:
        """
            Add updates board by iterating to next value of state
        :param x: horizontal coordinate of the board
        :param y: vertical coordinate of the board
        """
        self.board[y, x] = (self.board[x, y] - 1) % 4

    def set(self, x: int, y: int, v: int) -> None:
        """
            Set updates the board position x, y with value v
        :param x: horizontal coordinate of the board
        :param y: vertical coordinate of the board
        :param v: value to put in place
        """
        self.board[y, x] = v

    def next(self):
        """
            Next updates the game to the new state
        """
        # New board for new state
        new_board = np.zeros_like(self.board)

        # conductor -> head if on or two neighbours are electrons, else -> conductor
        conductors = np.where(self.board == CONDUCTOR)
        for i in range(len(conductors[0])):
            y, x = conductors[0][i], conductors[1][i]
            # iteration over all conductors
            neighbours = neighbourhood.moore_hard(self.board, x, y)
            if np.count_nonzero(neighbours == ELECTRON_HEAD) in [1, 2]:
                new_board[y, x] = ELECTRON_HEAD
            else:
                new_board[y, x] = CONDUCTOR
        # head -> tail
        new_board[self.board == ELECTRON_HEAD] = ELECTRON_TAIL
        # tail -> conductor
        new_board[self.board == ELECTRON_TAIL] = CONDUCTOR
        self.board = new_board

    def get_board(self, x: int, y: int, width: int = -1, height: int = -1, pad: bool = False) -> np.ndarray:
        """
            get_board returns part of the board as numpy.ndarray
        :param x: horizontal element of the top left element to return
        :param y: vertical element of the top left element to return
        :param width: width of the returned board
        :param height: height of the returned board
        :param pad: whether the resulting array should be padded
        :return:
        """
        if width == -1:
            width = self.board.shape[1]
        if height == -1:
            height = self.board.shape[0]
        board = self.board[y:y + height, x:x + width]
        if pad:
            h, w = board.shape
            board = np.pad(board, ((0, max(0, height - h)), (0, width - w)))
        return board

    def expand_board(self, x1: int, x2: int, y1: int, y2: int) -> None:
        """
            expand_board expands the board in 4 direction
        :param x1: expansion to the left
        :param x2: expansion to the right
        :param y1: expansion to the top
        :param y2: expansion to the bottom
        """
        self.board = np.pad(self.board, ((y1, y2), (x1, x2)))

    @staticmethod
    def get_color_dict() -> dict:
        """
            get_color_dict return the dictionary containing translations from
            numpy board values to rgb color tuples
        """
        return {
            0: (0, 0, 0), 1: (0, 0, 255), 2: (255, 0, 0), 3: (255, 255, 0),
        }

    @staticmethod
    def color_table() -> list:
        return [(0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0)]

    @staticmethod
    def possible_values() -> list:
        return [
            ("Conductor", CONDUCTOR),
            ("Electron Head", ELECTRON_HEAD),
            ("Electron Tail", ELECTRON_TAIL),
        ]

    def get_board_size(self) -> tuple:
        height, width = self.board.shape
        return width, height

    def load_board(self, filename: str):
        board = np.load(filename)
        self.board = board

    def save_board(self, filename: str):
        np.save(filename, self.board)


if __name__ == "__main__":
    b = np.array([[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 3, 0, 0], [0, 3, 0, 0, 0, 3, 0], [0, 0, 3, 3, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]], dtype=np.int8)
    game = WireWorld(b)
    print(game.get_board(0, 0, 15, 20))
    print(game.get_board(0, 0, 15, 20).shape)
    #
    # while True:
    #     game.next()
    #     print(game.get_board(1, 1, 3, 5))
    #     time.sleep(1)
