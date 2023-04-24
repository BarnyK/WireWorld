import numpy as np


def moore_pad(arr: np.ndarray, x: int, y: int):
    padded_arr = np.pad(arr, 1, mode='constant', constant_values=0)
    window = padded_arr[x:x + 3, y:y + 3]
    return window.flatten()


def moore_hard(arr: np.ndarray, x: int, y: int):
    mx, my = arr.shape
    neighbours = [(x + i, y + j) for i in range(-1, 2, 1) for j in range(-1, 2, 1)]
    neighbours = [(x, y) for x, y in neighbours if x >= 0 and y >= 0]
    neighbours = [(x, y) for x, y in neighbours if x < mx and y < my]
    neighbours.remove((x, y))
    x_coords, y_coords = zip(*neighbours)

    return arr[x_coords, y_coords]


if __name__ == "__main__":
    test_matrix = np.zeros((4, 4))
    test_matrix[0, 0] = 1
    test_matrix[1, 1] = 3
    test_matrix[2, 2] = 5
    test_matrix[3, 3] = 7

    a = moore_hard(test_matrix, 3, 3)
    print((a == 0).sum())
