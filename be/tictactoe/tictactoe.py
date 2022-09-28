
# Constants
from typing import Set, Tuple

from tictactoe.exceptions import BoardException, CordException


VALUE_EMPTY = None
VALUE_O = 0
VALUE_X = 1

WIN_STATUS = 1
NONE_STATUS = 0

DIRECTIONS = (
    (0, 1), #  RIGHT
    (1, 1), #  RIGHT-DOWN
    (1, 0), #  DOWN
    (1, -1), #  LEFT-DOWN
    )
    

class Cell:
    def __init__(self) -> None:
        self._value = VALUE_EMPTY

    @property
    def value(self):
        """Cell value getter"""
        return self._value

    @value.setter
    def value(self, value):
        """Cell value setter"""
        self._value = value


class TicTacToe:
    def __init__(self, board_size=3, win_size=3) -> None:
        
        self._validate_size(board_size, win_size)
        self._size = board_size
        self._win_size = win_size
        self._board = self._create_board()
        self._win_cords = self._create_win_cords()


    def _validate_size(self, board_size: int, win_size: int):
        """Validation for sizes"""
        if win_size > board_size:
            raise BoardException(
                "Board size should be bigger or equal then win size"
                )
        if win_size <= 0 or board_size <= 0:
            raise BoardException(
                "Sizes should be bigger than zero"
            )
        if win_size == 1:
            raise BoardException(
                "Win size should be bigger than one"
            )


    def _create_board(self):
        """Create board [size x size]"""
        return [
            [Cell() for _ in range(self._size)] 
            for _ in range(self._size)
        ]
    

    def change_cell_value(self, cord: Tuple[int, int], value: int):
        """Set X or O to Cell by cords"""
        i, j = cord
        self._board[i][j].value = value
        return self.check_win_status()


    def check_win_status(self):
        """
        Checks if one of players win and returns message with game status: \n
        (0 - In game, 1 - Game ends)
        """
        for win_line in self._win_cords:
            i, j = win_line[0]
            result = self._board[i][j]
            win_flag = True if result.value is not VALUE_EMPTY else False
            for i, j in win_line[1:]:
                if result.value != self._board[i][j].value:
                    win_flag = False
                    break
                if self._board[i][j].value == VALUE_EMPTY:
                    win_flag = False
            if win_flag:
                return {
                    "status": WIN_STATUS,
                    "data": {
                        "winner": result.value, 
                        "win_line": win_line
                        }
                    }

        return {
            "status": NONE_STATUS,
            "data": None
        }
            

    def _is_cord_on_board(self, i: int, j: int) -> bool:
        """
        Checks if coord is part of game board
        """
        i_condition = (i >= 0 and i  < self._size) 
        j_condition = (j >= 0 and j < self._size)
        return i_condition and j_condition


    def _create_cord_line(self, direction, i: int, j: int)-> Tuple[Tuple]: 
        """
        Create cord line from start_point[i][j] by direction with 
        length of win size
        """
        cord = list()
        for k in range(self._win_size):
            i_k = i + direction[0] * k
            j_k = j + direction[1] * k
            if self._is_cord_on_board(i_k, j_k):
                cord.append((i_k, j_k))
            else:
                raise CordException("Cord out of bounds")
        return tuple(cord)

    def _create_win_cords(self) -> Set[Tuple[Tuple[int, int]]]:
        """
        Returns set of winning combinations
        """
        win_cords = list()
        for i in range(self._size):
            for j in range(self._size):
                for dir in DIRECTIONS:
                    try:
                        win_cords.append(self._create_cord_line(dir, i, j))
                    except CordException:
                        continue
        
        return set(win_cords)
                        

    def draw_table(self):
        """
        Prints board
        """
        for i in range(self._size):
            for j in range(self._size):
                value = self._board[i][j].value
                if value == VALUE_EMPTY:
                    print(".", end=" ")
                if value == VALUE_O:
                    print("O", end=" ")
                if value == VALUE_X:
                    print("X", end=" ")
            print()
