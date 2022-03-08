import numpy as np
import matplotlib.pyplot as plt


def plot_solution(board_size, shapes, problem_solution, vacant_squares=False):
    board_solved = np.zeros(board_size)

    if vacant_squares:
        shapes.append("#")

    for piece in problem_solution:
        value = np.where(piece[:len(shapes)] == 1)[0][0]
        board_solved += np.reshape(piece[len(shapes):], board_size) * value

    fig, ax = plt.subplots()

    im = ax.imshow(board_solved, cmap="prism")

    for i in range(board_solved.shape[0]):
        for j in range(board_solved.shape[1]):
            ax.text(j, i, shapes[int(board_solved[i, j])],
                ha="center", va="center", color="k")

    plt.show()


if __name__ == "__main__":
    shapes = ["Y", "N", "L", "P", "V"]
    problem_solution = np.array([
        [1., 0., 0., 0., 0., 1., 1., 1., 1., 0., 1., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 1., 1., 0.,
        0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0.],
       [0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
        0., 0., 0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 1., 1.],
       [0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 0., 0.,
        1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.,
        0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 1., 1., 0., 0.]]
    )
    plot_solution(board_size=(5, 5), shapes=shapes, problem_solution=problem_solution)
