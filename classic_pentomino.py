import numpy as np

from dlx_algorithm import DLX
from plot_solution import plot_solution
from polymino_cover_problem import polymino_cover_problem

if __name__ == "__main__":
    board_size = (6, 10) # (5, 12) , (4, 15) , (3, 20)
    vacant_squares = []
    shapes = ["F", "I", "L", "N", "P", "T", "U", "V", "W", "X", "Y", "Z"]

    cover_matrix = polymino_cover_problem(
        board_size=board_size, vacant_squares=vacant_squares, shapes=shapes
    )

    problem = DLX(input_matrix=cover_matrix)
    solution = problem.solve()

    if solution[0]:
        print("Problema resolvido!, plotando solução")
        plot_solution(board_size=board_size, shapes=shapes, problem_solution=solution[1])
    else:
        print("Não foi possível resolver o problema")
