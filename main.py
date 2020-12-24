from collections import OrderedDict
from typing import List, Tuple, Set

from PIL import Image
import pyautogui

BOARD_LENGTH = 9
BOARD_HEIGHT = 9

BOARD_WALL_RGB = (128, 128, 128)
BOARD_POSITION = (1399, 383, 1612, 596)
BOX_SIZE = 21
BOX_DELIMITER_SIZE = 2

BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (253, 4, 6)
EXPLODE_COLOR = (245, 137, 138)
BOMB_COLOR = (209, 209, 209)
DISCOVERED_COLOR = (187, 193, 255)
UNDISCOVERED_COLORS = [
    (0, 103, 96),
    (4, 183, 173),
]

BOXES_COLORS = OrderedDict(
    [
        ("1", [BLUE, DISCOVERED_COLOR]),
        ("2", [GREEN, DISCOVERED_COLOR]),
        ("3", [RED, DISCOVERED_COLOR]),
        ("bomb", [BOMB_COLOR] + UNDISCOVERED_COLORS),
        ("exploded_bomb", [EXPLODE_COLOR, BOMB_COLOR]),
        ("X", UNDISCOVERED_COLORS),
        ("0", [DISCOVERED_COLOR]),
    ]
)


def main():
    # for entering the loop
    non_bombs = [1]
    while non_bombs:
        board = capture_board()
        board = mark_board(board)
        bombs = find_bombs(board)
        non_bombs = find_non_bombs(bombs, board)
        click_all(non_bombs)


def click_all(positions: List[Tuple[int, int]]):
    for p in positions:
        print(p[0], p[1])
        click(p[0], p[1])


def click(row: int, col: int):
    x = BOARD_POSITION[0] + (col * (BOX_SIZE + BOX_DELIMITER_SIZE)) + 10
    y = BOARD_POSITION[1] + (row * (BOX_SIZE + BOX_DELIMITER_SIZE)) + 10

    pyautogui.click(x=x, y=y)


def find_non_bombs(bombs: List[Tuple[int, int]], board: List[List[str]]):
    non_bombs = set()
    for row_index, row in enumerate(board):
        for col_index, mark in enumerate(row):
            if mark.isnumeric() and mark != "0":
                for bomb in find_non_bombs_around(
                    int(mark), row_index, col_index, board, bombs
                ):
                    non_bombs.add(bomb)
    return list(non_bombs)


def get_undiscovered_boxes_around(row: int, col: int, board: List[List[str]]):
    around = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]
    # removes boxes that are out of bound
    return [
        loc
        for loc in around
        if 0 <= loc[0] < len(board)
        and 0 <= loc[1] < len(board[0])
        and board[loc[0]][loc[1]] == "X"
    ]


def find_non_bombs_around(
    num: int, row: int, col: int, board: List[List[str]], bombs: List[Tuple[int, int]]
):
    around = get_undiscovered_boxes_around(row, col, board)
    non_bombs = [box for box in around if box not in bombs]
    bombs_amount_around = len(around) - len(non_bombs)
    return non_bombs if num == bombs_amount_around else []


def find_bombs_around(num: int, row: int, col: int, board: List[List[str]]):
    around = get_undiscovered_boxes_around(row, col, board)
    return around if num == len(around) else []


def find_bombs(board: List[List[str]]):
    bombs = set()
    for row_index, row in enumerate(board):
        for col_index, mark in enumerate(row):
            if mark.isnumeric() and mark != "0":
                for bomb in find_bombs_around(int(mark), row_index, col_index, board):
                    bombs.add(bomb)
    return list(bombs)


def print_board(board: List[List[str]]):
    for row in board:
        for mark in row:
            print(mark, end=" ")
        print()


def mark_board(board: List[List[Image.Image]]) -> List[List[str]]:
    return [[mark_box(box) for box in row] for row in board]


def mark_box(box: Image.Image) -> str:
    pixels = list(box.getdata())
    for box_mark in BOXES_COLORS.keys():
        if all(color in pixels for color in BOXES_COLORS[box_mark]):
            return box_mark

    raise UnrecognizedBoxException()


def capture_board():
    full_screen = pyautogui.screenshot()
    board = full_screen.crop(box=BOARD_POSITION)

    return [
        [
            board.crop((x, y, x + BOX_SIZE, y + BOX_SIZE))
            for x in range(0, board.size[0], BOX_SIZE + BOX_DELIMITER_SIZE + 1)
        ]
        for y in range(0, board.size[1], BOX_SIZE + BOX_DELIMITER_SIZE + 1)
    ]


if __name__ == "__main__":
    main()


class UnrecognizedBoxException(Exception):
    pass
