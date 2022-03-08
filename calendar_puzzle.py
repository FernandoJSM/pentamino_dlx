import numpy as np

from dlx_algorithm import DLX
from plot_solution import plot_solution
from polymino_cover_problem import polymino_cover_problem

if __name__ == "__main__":
    month = 3
    day = 1

    m_i, m_j = np.where(np.reshape(np.array(range(1, 13)), (2, 6)) == month)
    month_pos = (m_i[0], m_j[0])

    d_i, d_j = np.where(np.reshape(np.array(range(1, 36)), (5, 7)) == day)
    day_pos = (d_i[0] + 2, d_j[0])

    board_size = (7, 7)
    vacant_squares = [(0, 6), (1, 6), (6, 3), (6, 4), (6, 5), (6, 6), month_pos, day_pos]
    shapes = ["L", "N", "O", "P", "U", "V", "Y", "Z"]

    cover_matrix = polymino_cover_problem(
        board_size=board_size, vacant_squares=vacant_squares, shapes=shapes
    )

    problem = DLX(input_matrix=cover_matrix)
    solution = problem.solve()

    if solution[0]:
        print("Problema resolvido!, plotando solução")
        plot_solution(board_size=board_size, shapes=shapes, problem_solution=solution[1], vacant_squares=True)
    else:
        print("Não foi possível resolver o problema")
