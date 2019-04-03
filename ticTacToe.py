class Player(object):
    next_player_val = {'O': 'X', 'X': 'O'}

    def __init__(self, val='O'):
        self.val = val

    def get_move_input(self, board_size):
        """
        :raises ValueError: raises an exception
        """
        input_raw = raw_input(
            "\nHi player %s. Input x,y to make a move, where 0 <= x,y <= %s: " % (self.val, str(board_size-1))
        )
        i, j = map(int, input_raw.split(","))
        if not 0 <= i < board_size or not 0 <= j < board_size:
            raise ValueError()
        else:
            return i, j

    def quit(self):
        input_raw = raw_input("The move is not legitimate. Would you like to quit the game? (y/N)\n")
        if 'Y' == input_raw.capitalize():
            print("\nSee ya!\n")
            return True
        else:
            return False

    def next_round(self):
        self.val = self.next_player_val[self.val]


class TicTacToe(object):
    def __init__(self, player, board_size=3):
        self.board_size = board_size
        self.board = [["_"] * board_size for _ in range(board_size)]
        self.player = player
        self.moves = 0
        self.current_input = None
        # record (cnt O, cnt X) for O(1) check_result
        self.row_stat = [{"O": 0, "X": 0} for _ in range(board_size)]
        self.col_stat = [{"O": 0, "X": 0} for _ in range(board_size)]
        self.diag_stat = {"O": 0, "X": 0}
        self.diag2_stat = {"O": 0, "X": 0}

    def is_over(self):
        if not self.moves:
            return False
        elif self.moves == self.board_size * self.board_size:
            print("It's a draw. No one wins.")
            return True
        elif self._check_diag() or self._check_row_col():
            print("Player %s wins!" % player.val)
            return True
        else:
            return False

    def _check_diag(self):
        i, j = self.current_input
        val = self.board[i][j]

        if (i == j) and (self.board_size == self.diag_stat[val]):
            return True
        if (j == self.board_size - i - 1) and (self.board_size == self.diag2_stat[val]):
            return True

        return False

    def _check_row_col(self):
        i, j = self.current_input
        val = self.board[i][j]

        return self.board_size in (self.row_stat[i][val], self.col_stat[j][val])

    def make_move(self, i, j, val):
        """
        val should be string O or X
        """
        if self.board[i][j] != '_':
            print("This spot (%d,%d) is already occupied! Make another legitimate move instead.\n" % (i, j))
            return False

        self.current_input = i, j
        self.board[i][j] = val
        self.moves += 1

        self.row_stat[i][val] += 1
        self.col_stat[j][val] += 1
        if i == j:
            self.diag_stat[val] += 1
        if j == self.board_size - i - 1:
            self.diag2_stat[val] += 1
        # print(i, j, val, self.row_stat, self.col_stat)
        return True

    def output_board(self):
        for i in range(self.board_size):
            print(",".join(self.board[i]))


if __name__ == '__main__':
    player = Player()
    game = TicTacToe(player)
    is_move_valid = False

    while not game.is_over():
        if is_move_valid:
            player.next_round()

        try:
            x, y = player.get_move_input(game.board_size)
        except ValueError:
            if player.quit():
                exit()
            else:
                is_move_valid = False
                continue

        is_move_valid = game.make_move(x, y, player.val)
        if is_move_valid:
            game.output_board()
        else:
            continue
