import copy

class Puzzle:
    def __init__(self, L_M, L_C):
        self.L_M = L_M
        self.L_C = L_C
        self.R_M = 0
        self.R_C = 0
        self.P_B = 'L'
        # この上の変数群は基本、init以外のメソッドでは呼び出さない！

        self.board_start = [self.L_M, self.L_C, self.R_M, self.R_C, self.P_B]
        self.board_goal = [self.R_M, self.R_C, self.L_M, self.L_C, 'R' if self.P_B == 'L' else 'L']
        self.open = [self.board_start]
        self.closed = []
        self.board_current = []

        self.condition = []
        self.L_to_R_patterns = [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]
        self.R_to_L_patterns = [[0, -1], [0, -2], [-1, 0], [-1, -1], [-2, 0]]

    def print_board(self):
        print(self.board_current)
    
    def set_condition(self):
        self.condition.append(lambda board: board[0] >= board[1] or board[0] == 0)
        self.condition.append(lambda board: board[2] >= board[3] or board[2] == 0)
        self.condition.append(lambda board: all(value >= 0 for value in board[:4]))
        # self.condition.append(lambda board: board in self.open)
        self.condition.append(lambda board: board not in self.closed)

    def forward(self):
        # openの最後の要素を取り出す！
        self.board_current = self.open.pop() # エラーに注意！
        if self.board_current in self.closed:
            return # 次のforward（つまり次の要素の取り出し）へ
        self.closed.append(self.board_current)

        # 探索中のノードの出力
        print(self.board_current)

        if self.board_current[4] == 'L':
            for pattern in self.L_to_R_patterns:
                new_board = copy.deepcopy(self.board_current)
                new_board[0] -= pattern[0]
                new_board[2] += pattern[0]
                new_board[1] -= pattern[1]
                new_board[3] += pattern[1]
                new_board[4] = 'R'
                if new_board == self.board_goal:
                    print(new_board)
                    print("Finished!")
                    return 1
                elif all(check(new_board) for check in self.condition):
                    self.open.append(new_board)

        elif self.board_current[4] == 'R':
            for pattern in self.R_to_L_patterns:
                new_board = copy.deepcopy(self.board_current)
                new_board[0] -= pattern[0]
                new_board[2] += pattern[0]
                new_board[1] -= pattern[1]
                new_board[3] += pattern[1]
                new_board[4] = 'L'
                if all(check(new_board) for check in self.condition):
                    self.open.append(new_board)

        return

    def search(self):
        self.set_condition()
        while self.open:
            res = self.forward()
            if res == 1:
              break


def main():
    newPuzzle = Puzzle(2, 2)
    newPuzzle.search()


if __name__ == "__main__":
    main()
