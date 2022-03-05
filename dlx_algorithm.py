import numpy as np
import string


class DLX:

    def __init__(self, input_matrix, column_names=None):
        self.matrix = input_matrix
        self.shape = input_matrix.shape
        self.column_names = column_names if column_names is not None else list(string.ascii_uppercase)[0:self.shape[1]]

        fields_shape = self.shape + (2,)
        self.L = np.ones(shape=fields_shape) * -1
        self.R = np.ones(shape=fields_shape) * -1
        self.U = np.ones(shape=fields_shape) * -1
        self.D = np.ones(shape=fields_shape) * -1
        self.S = np.sum(self.matrix, axis=0)

        self.H = np.ones(shape=self.shape[1]+1)  # Active headers (root h + columns)
        self.LH = np.ones(shape=self.H.shape)
        self.RH = np.ones(shape=self.H.shape)

        self.build_fields()

    @staticmethod
    def find_ones(array, start_index, right):
        """
            Return the index of the first one in left or right from the start index
        """
        j = start_index
        for c in range(len(array)):
            if right:
                j = j + 1 if j + 1 < len(array) else 0
            else:
                j = j - 1 if j - 1 > -1 else len(array) - 1

            if array[j] == 1:
                return j
        return -1

    def build_fields(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.matrix[i, j] == 0:
                    continue

                find_left = self.find_ones(array=self.matrix[i, :], start_index=j, right=False)
                if find_left > -1:
                    self.L[i, j] = (i, find_left)

                find_right = self.find_ones(array=self.matrix[i, :], start_index=j, right=True)
                if find_right > -1:
                    self.R[i, j] = (i, find_right)

                find_up = self.find_ones(array=self.matrix[:, j], start_index=i, right=False)
                if find_up > -1:
                    self.U[i, j] = (find_up, j)

                find_down = self.find_ones(array=self.matrix[:, j], start_index=i, right=True)
                if find_down > -1:
                    self.D[i, j] = (find_down, j)

        self.LH = np.array(range(self.H.shape[0])) - 1
        self.LH[0] = self.H.shape[0] - 1
        self.RH = np.array(range(self.H.shape[0])) + 1
        self.RH[-1] = 0

    def solve(self, k=0):
        if np.array_equal(self.RH, np.array([0])):
            return #===============================

        # Choosing a column
        c = None
        s = np.inf
        for j in np.where(self.RH > 0)[0]:
            if self.S[j] < s:
                c = j
                s = self.S[j]

        # Covering column c
        a=1

if __name__ == "__main__":
    DLX(input_matrix=np.array([
        [0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
    ])).solve()
