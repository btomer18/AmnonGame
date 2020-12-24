from PIL import Image
import pyautogui

BOARD_LENGTH = 9
BOARD_HEIGHT = 9

BOARD_WALL_RGB = (128, 128, 128)
BOARD_POSITION = (1411, 274, 1626, 489)
BOX_SIZE_PX = 24


def main():
    board = capture_board()


def capture_board():
    full_screen = pyautogui.screenshot()
    board = full_screen.crop(box=BOARD_POSITION)

    return [
        [
            board.crop((x, y, x + BOX_SIZE_PX, y + BOX_SIZE_PX))
            for x in range(0, board.size[0], BOX_SIZE_PX)
        ]
        for y in range(0, board.size[1], BOX_SIZE_PX)
    ]


if __name__ == "__main__":
    main()
