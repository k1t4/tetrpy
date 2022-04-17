import random
from enum import Enum

from matrix import Matrix


# todo beautify somehow
class TetrominoType(Enum):
    I = [
         [[1, 1, 2, 1]],
         [[1],
          [1],
          [2],
          [1]]
    ]

    O = [
         [[2, 1],
          [1, 1]]
        ]

    T = [[[1, 2, 1],
          [0, 1, 0]],
         [[0, 1, 0],
          [1, 2, 1]],
         [[1, 0],
          [2, 1],
          [1, 0]],
         [[0, 1],
          [1, 2],
          [0, 1]]]

    J = [
         [[0, 1],
          [0, 2],
          [1, 1]],
         [[1, 2, 1],
          [0, 0, 1]],
         [[1, 1],
          [2, 0],
          [1, 0]],
         [[1, 0, 0],
          [1, 2, 1]]
    ]

    L = [
         [[1, 0],
          [2, 0],
          [1, 1]],
         [[0, 0, 1],
          [1, 2, 1]],
         [[1, 1],
          [0, 2],
          [0, 1]],
         [[1, 2, 1],
          [1, 0, 0]]
        ]

    S = [
         [[0, 1, 1],
          [1, 2, 0]],
         [[1, 0],
          [1, 2],
          [0, 1]],
        ]

    Z = [
         [[1, 1, 0],
          [0, 2, 1]],
         [[0, 1],
          [1, 2],
          [1, 0]]
    ]


class Tetromino(Matrix):
    def __init__(self, figure_type_class=None):
        if not figure_type_class:
            figure_type_class = random.choice(list(TetrominoType)).value
            type_index = random.choice(range(len(figure_type_class)))
            figure_type_matrix = figure_type_class[type_index]
        else:
            type_index = 0
            figure_type_matrix = figure_type_class[type_index]

        self.figure_type_class = figure_type_class
        self.type_index = type_index

        self.x = 0
        self.y = 0

        super().__init__(list_=figure_type_matrix)

    def rotate(self):
        center_y, center_x = self.get_relative_center_coordinates()
        # choose next figure type
        self.type_index = (self.type_index + 1) % len(self.figure_type_class)
        figure_type_matrix = self.figure_type_class[self.type_index]
        self.list = figure_type_matrix

        center_y_new, center_x_new = self.get_relative_center_coordinates()

        shift_y = center_y - center_y_new
        self.y += shift_y

        shift_x = center_x - center_x_new
        self.x += shift_x

    def get_relative_center_coordinates(self):
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self[y][x] == 2:
                    return y, x

    def _expand_matrix(self):
        """
        Converts given matrix to 4x4 matrix
        """
        num_of_rows_to_add = 4 - self.size_y
        num_of_cols_to_add = 4 - self.size_x

        for _ in range(num_of_rows_to_add):
            self.list.append([0 for __ in range(self.size_x)])

        for y in range(self.size_y):
            for __ in range(num_of_cols_to_add):
                self[y].append(0)

    def _reduce_matrix(self):
        for y in range(self.size_y - 1, 0, -1):
            if not any(self[y]):
                del self.list[y]

        for _ in range(self.size_x):
            last_elements = [row[-1] for row in self.list]
            if not any(last_elements):
                for row in self.list:
                    del row[-1]
            else:
                return
