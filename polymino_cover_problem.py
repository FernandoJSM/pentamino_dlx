import numpy as np
import itertools
from pentaminoes import Pentaminoes


def polymino_cover_problem(board_size, vacant_squares=[], shapes=[]):
    board = np.zeros(board_size)
    board_shape = np.array(board.shape)
    positions = list(itertools.product(range(board.shape[0]), range(board.shape[1])))

    placed_pieces = list()

    for s, shape_name in enumerate(shapes):

        for piece in Pentaminoes.pieces[shape_name]:
            piece_shape = np.array(piece.shape)

            for position in positions:
                if np.any(piece_shape + position > board_shape):
                    # Piece doesn't fit the board
                    continue

                piece_in_board = board.copy()
                piece_in_board[position[0]:position[0]+piece.shape[0], position[1]:position[1]+piece.shape[1]] = piece

                if np.where(piece_in_board > 1)[0].size == 0:
                    placed_pieces.append((s, piece_in_board.flatten()))

    pieces_matrix = np.zeros((len(placed_pieces), len(set(pp[0] for pp in placed_pieces))))
    positions_matrix = np.zeros((len(placed_pieces), len(placed_pieces[0][1])))

    for i, pp in enumerate(placed_pieces):
        pieces_matrix[i][pp[0]] = 1
        positions_matrix[i] = pp[1]

    cover_matrix = np.hstack((pieces_matrix, positions_matrix))

    return cover_matrix


if __name__ == "__main__":
    from dlx_algorithm import DLX

    cover_matrix = polymino_cover_problem(
        board_size=(5, 5), vacant_squares=[], shapes=["L", "N", "P", "V", "Y"]
    )

    problem = DLX(input_matrix=cover_matrix)
    solution = problem.solve()
    print(solution[1])