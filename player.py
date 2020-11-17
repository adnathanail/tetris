from board import Direction, Rotation, Board
from random import Random

from exceptions import NoBlockException


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def get_score_from_board(self, board):
        # Parse board cells into 2D array of 1's and 0's
        board_useful = [[0 for _ in range(board.width)] for _ in range(board.height)]  # Initialise 2D array of 0's
        for x, y in board:
            board_useful[y][x] = 1

        # Column heights (used by total height and height differences)
        column_heights = {}
        for x in range(board.width):
            max_y = 0
            for y in range(board.height):
                if board_useful[y][x] == 1:
                    max_y = board.height - y
                    break
            column_heights[x] = max_y

        # Height of all columns added together
        total_height = sum(column_heights[col] for col in column_heights)
        # Total difference between adjacent columns heights
        height_differences = sum(
            abs(column_heights[i + 1] - column_heights[i])
            for i in range(board.width - 1)
        )
        # Number of rows that would end up disappearing
        complete_rows = 0
        for y in range(board.height):
            all_filled = all(board_useful[y][x] != 0 for x in range(board.width))
            if all_filled:
                complete_rows += 1
        # Number of gaps left in the grid
        holes = 0
        for y in range(1, board.height):
            for x in range(board.width):
                if board_useful[y][x] == 0 and board_useful[y - 1][x] == 1:
                    holes += 1

        return (complete_rows * 760) - (holes * 356) - (height_differences * 184) - (total_height * 510)

    def choose_action(self, board: Board):
        best_score = None
        best_moves = None
        for r in range(4):  # rotation
            for x in range(10):  # x-coord
                moves = []
                # Generate rotation moves
                if r <= 2:
                    for _ in range(r):
                        moves.append(Rotation.Clockwise)
                else:
                    moves.append(Rotation.Anticlockwise)
                # Generate direction moves
                x_offset = x - board.falling.center[0]  # difference between current x and target x
                if type(board.falling.center[0]) == float:
                    x_offset += 0.5
                for _ in range(abs(int(x_offset))):
                    if x_offset > 0:
                        moves.append(Direction.Right)
                    else:
                        moves.append(Direction.Left)
                moves.append(Direction.Drop)

                # Apply the moves to a copy of the board
                try:
                    b = board.clone()
                    for move in moves:
                        if isinstance(move, Direction):
                            b.move(move)
                        elif isinstance(move, Rotation):
                            b.rotate(move)

                    b.pprint()
                    s = self.get_score_from_board(b)
                    if best_score is None or s > best_score:
                        best_score = s
                        best_moves = moves
                except NoBlockException:
                    continue

        return best_moves


SelectedPlayer = RandomPlayer
