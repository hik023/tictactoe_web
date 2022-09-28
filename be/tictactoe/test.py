import os

from tictactoe import TicTacToe, WIN_STATUS


def game_loop(ttt: TicTacToe, player):
    while True:
        os.system("clear")
        ttt.draw_table()
        i, j = input("Choose cell (i j): ").split(" ")
        cord = (int(i), int(j))
        p = 1 if player else 0
        result = ttt.change_cell_value(cord, p)
        if result["status"] == WIN_STATUS:
            print(f"Player {result['data']['winner']} "\
            f"Win with {result['data']['win_line']}")
            break
        player = not player


if __name__ == "__main__":
    ttt = TicTacToe(5,3)
    player = True
    game_loop(ttt, player)

