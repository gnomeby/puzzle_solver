from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class Piece(list):
    def __hash__(self):
        return hash('|'.join(self))

color_map = {'B': Fore.BLUE, 'R': Fore.RED, 'Y': Fore.YELLOW, 'G': Fore.GREEN,
                'C': Fore.CYAN, 'O': Fore.LIGHTRED_EX, ' ': Fore.RESET, 'D': Fore.LIGHTBLACK_EX}

pieces = [
    Piece(( "B B",  # Blues
            "BBB")),

    Piece(( " R ",  # Red
            "RRR")),

    Piece(( " R ",
            "RRR")),

    Piece(( "GG ",  # Green
            " GG")),

    Piece(( "GG ",
            " GG")),

    Piece(( "DDDD",)),# Dark

    Piece(( "YY",   # Yellow
            "YY")),

    Piece(( "CCC",  # Violet
            "C  ")),

    Piece(( "OO",   # Orange
            "O ")),
]

board = [" " * 6] * 6
complexity = 0


def rotate(piece: list, x: int = 0, y: int = 0, z: int = 0) -> list:
    assert x % 90 == 0
    assert y % 90 == 0
    assert z % 90 == 0
    assert not (x > 0 and y > 0)
    assert x in [0, 180]
    assert y == 0
    assert z in [0, 90, 180, 270]

    new_piece = Piece(piece.copy())

    while z > 0:
        w = len(new_piece[0])
        h = len(new_piece)

        after_rotate = [bytearray(b' ' * h).copy() for i in range(w)]

        for i in range(w):
            for j in range(h):
                after_rotate[i][-1-j] = ord(new_piece[j][i])

        new_piece = Piece((line.decode() for line in after_rotate))
        z -= 90

    # import pudb;pudb.set_trace()

    if x == 180:
        for i in range(len(new_piece) // 2):
            new_piece[i], new_piece[-1-i] = new_piece[-i-1], new_piece[i]

    return new_piece

def get_possible_rotations(piece: list) -> list:
    pieces = []
    for x in [0, 180]:
        for z in [0, 90, 180, 270]:
            pieces.append(rotate(piece, x=x, z=z))

    return set(pieces)

def insert_into_board(board: list, piece: list) -> iter:
    for i in range(len(board[0]) - len(piece[0]) + 1):
        for j in range(len(board) - len(piece) + 1):
            new_board = [bytearray(line.encode('ascii')) for line in board]
            try:
                for k in range(len(piece[0])):
                    for l in range(len(piece)):

                        if piece[l][k] == ' ':
                            continue
                        elif new_board[j+l][i+k] == ord(' '):
                            new_board[j+l][i+k] = ord(piece[l][k])
                            continue
                        else:
                            raise ValueError()

                yield [line.decode() for line in new_board]
            except ValueError:
                continue

def next_step(board: list, pieces: list):
    global complexity
    complexity += 1
    # import pudb;pudb.set_trace()
    if not pieces:
        print_board(board)
        print("Complexity", complexity)
        return

    for piece in get_possible_rotations(pieces[0]):
        for new_board in insert_into_board(board, piece):
            next_step(new_board, pieces[1:])
    pass

def print_piece(piece: list):
    for line in piece:
        for ch in line:
            print(f"{color_map[ch]}{ch}{Style.RESET_ALL}", end='')
        print()

def print_board(board: list):
    # Print board
    print("Result:")
    print(' ' + '_' * len(board[0]) + ' ')
    for line in board:
        print("|", end='')
        for ch in line:
            print(f"{color_map[ch]}{ch}{Style.RESET_ALL}", end='')
        print("|", end='')

        print()
    print(' ' + '-' * len(board[0]) + ' ')


if __name__ == "__main__":
    next_step(board, pieces.copy())
