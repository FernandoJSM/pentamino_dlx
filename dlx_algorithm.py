from dataclasses import dataclass

import numpy as np
import string


@dataclass
class Element:
    pos: tuple = (-1, -1)
    covered: bool = False

    L: tuple = (-1, -1)
    R: tuple = (-1, -1)
    U: tuple = (-1, -1)
    D: tuple = (-1, -1)
    C: tuple = (-1, -1)

    is_header: bool = False
    N: string = ""
    S: int = -1


class DLX:
    def __init__(self, input_matrix: np.ndarray):
        self.input_matrix = input_matrix
        self.matrix = list()
        self.shape = input_matrix.shape
        self.column_names = list()
        self.solution = list()
        self.generate_column_names()
        self.build()

    def generate_column_names(self):
        alphabet_iteration = -1
        alphabet = string.ascii_uppercase
        for i in range(self.shape[1]):
            if i % 26 == 0:
                alphabet_iteration += 1
            self.column_names.append(alphabet[i % 26] + str(alphabet_iteration))

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

    def print_matrix(self, attribute=None):
        s = "    "
        for c, column in enumerate(self.column_names):
            s += "{0:^10s}".format(f"{c}-{column}") + "\t"
        print(s)
        for r, row in enumerate(self.matrix):
            s = f"{r} - "
            for field in row:
                text = "{0:^10s}".format("")
                if attribute is not None:
                    value = eval("field." + attribute)
                    if value != (-1, -1):
                        text = "{0:^10s}".format(f"({str(value[0])},{str(value[1])})")
                if field.covered:
                    text = "{0:^10s}".format("----")

                s += text + "\t"
            print(s)

    def build(self):
        self.matrix.append(list())
        for j in range(self.shape[1]):
            self.matrix[0].append(
                Element(
                    pos=(0, j),
                    L=(0, j - 1) if j - 1 > 0 else (0, self.shape[1] - 1),
                    R=(0, j + 1) if j + 1 < self.shape[1] else (0, 0),
                    C=(0, j),
                    is_header=True,
                    S=np.sum(self.input_matrix, axis=0)[j],
                    N=self.column_names[j],
                )
            )
        for i in range(self.shape[0]):
            self.matrix.append(list())
            for j in range(self.shape[1]):
                self.matrix[i + 1].append(
                    Element(pos=(i + 1, j), C=(0, j), N=self.column_names[j])
                )
                if self.input_matrix[i, j] == 0:
                    continue

                find_left = self.find_ones(
                    array=self.input_matrix[i, :], start_index=j, right=False
                )
                if find_left > -1:
                    self.matrix[i + 1][j].L = (i + 1, find_left)

                find_right = self.find_ones(
                    array=self.input_matrix[i, :], start_index=j, right=True
                )
                if find_right > -1:
                    self.matrix[i + 1][j].R = (i + 1, find_right)

                find_up = self.find_ones(
                    array=np.insert(self.input_matrix[:, j], 0, 1),
                    start_index=i + 1,
                    right=False,
                )
                if find_up > -1:
                    self.matrix[i + 1][j].U = (find_up, j)

                find_down = self.find_ones(
                    array=np.insert(self.input_matrix[:, j], 0, 1),
                    start_index=i + 1,
                    right=True,
                )
                if find_down > -1:
                    self.matrix[i + 1][j].D = (find_down, j)

        for j in range(self.shape[1]):
            find_up = self.find_ones(
                array=np.insert(self.input_matrix[:, j], 0, 1),
                start_index=0,
                right=False,
            )
            if find_up > -1:
                self.matrix[0][j].U = (find_up, j)

            find_down = self.find_ones(
                array=np.insert(self.input_matrix[:, j], 0, 1),
                start_index=0,
                right=True,
            )
            if find_down > -1:
                self.matrix[0][j].D = (find_down, j)

    def retrieve_elems(self, pos: tuple, attribute: str):
        """
        Retrieve a list of elements from the current position and attribute, excluding the current position element
        """
        elem_list = list()
        next_pos = eval("self.matrix[pos[0]][pos[1]]." + attribute)
        visited_pos = [next_pos]
        while next_pos != pos:
            elem_list.extend([self.matrix[next_pos[0]][next_pos[1]]])
            next_pos = eval("self.matrix[next_pos[0]][next_pos[1]]." + attribute)
            if next_pos in visited_pos:
                break
            visited_pos.append(next_pos)

        return elem_list

    def cover_column(self, c):
        # print(f"Covering column {c.pos[1]}")
        c.covered = True
        # Set L[R[c]] ← L[c] and R[L[c]] ← R[c].
        if c.R != (-1, -1):
            self.matrix[c.R[0]][c.R[1]].L = c.L

        if c.L != (-1, -1):
            self.matrix[c.L[0]][c.L[1]].R = c.R

        # For each i ← D[c], D[D[c]], ..., while i != c
        for i in self.retrieve_elems(pos=c.pos, attribute="D"):
            # For each j ← R[i], R[R[i]], ..., while j != i
            i.covered = True
            for j in self.retrieve_elems(pos=i.pos, attribute="R"):
                j.covered = True
                # set U[D[j]] ← U[j], D[U[j]] ← D[j]
                if j.D != (-1, -1):
                    self.matrix[j.D[0]][j.D[1]].U = j.U

                if j.U != (-1, -1):
                    self.matrix[j.U[0]][j.U[1]].D = j.D

                # set S[C[j]] ← S[C[j]] − 1
                self.matrix[j.C[0]][j.C[1]].S -= 1

    def uncover_column(self, c):
        c.covered = False
        # For each i = U[c], U[U[c]], ..., while i != c
        for i in self.retrieve_elems(pos=c.pos, attribute="U"):
            # for each j ← L[i], L[L[i]], ..., while j != i
            i.covered = False
            for j in self.retrieve_elems(pos=i.pos, attribute="L"):
                j.covered = False
                # set  S[C[j]] ← S[C[j]] + 1
                self.matrix[j.C[0]][j.C[1]].S += 1

                # set U[D[j]] ← j, D[U[j]] ← j
                if j.D != (-1, -1):
                    self.matrix[j.D[0]][j.D[1]].U = j.pos

                if j.U != (-1, -1):
                    self.matrix[j.U[0]][j.U[1]].D = j.pos

        # Set L[R[c]] ← c and R[L[c]] ← c
        if c.R != (-1, -1):
            self.matrix[c.R[0]][c.R[1]].L = c.pos

        if c.L != (-1, -1):
            self.matrix[c.L[0]][c.L[1]].R = c.pos

    def solve(self, k=0):
        # print(f"{k=}")
        if all([c.covered for c in self.matrix[0]]):
            return True, []

        # Choosing a column c
        c = None
        s = np.inf
        # for each j ← R[h], R[R[h]], ..., while j != h
        # There's no h field
        for j in [h for h in self.matrix[0] if h.covered is False]:
            # if S[j] < s set c ← j and s ← S[j]
            if j.S < s:
                c = j
                s = j.S

        # Covering column c
        self.cover_column(c=self.matrix[c.C[0]][c.C[1]])
        # For each r ← D[c], D[D[c]], ..., while r != c
        for r in self.retrieve_elems(pos=c.pos, attribute="D"):
            self.solution.append(self.input_matrix[r.pos[0] - 1])
            # for each j ← R[r], R[R[r]], ..., while j != r
            for j in self.retrieve_elems(pos=r.pos, attribute="R"):
                # Covering column j
                self.cover_column(c=self.matrix[j.C[0]][j.C[1]])

            if self.solve(k=k + 1)[0]:
                return True, np.array(self.solution)

            # set r ← Ok and c ← C[r]
            self.solution.pop(-1)
            # self.uncover_column(c=self.matrix[c.C[0]][c.C[1]])

            # for each j ← L[r], L[L[r]], ..., while j != r,
            for j in self.retrieve_elems(pos=r.pos, attribute="L"):
                # Uncovering column j
                self.uncover_column(c=self.matrix[j.C[0]][j.C[1]])

        self.uncover_column(c=self.matrix[c.C[0]][c.C[1]])

        return False, []


if __name__ == "__main__":
    problem = DLX(
        input_matrix=np.array(
            [
                [0, 0, 1, 0, 1, 1, 0],
                [1, 0, 0, 1, 0, 0, 1],
                [0, 1, 1, 0, 0, 1, 0],
                [1, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 1, 0, 1],
            ]
        )
    )

    solution = problem.solve()
    print(solution[1])
