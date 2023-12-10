import copy

class Puzzle:
    def __init__(self, N):
        self.N = N
        self.ship = 0
        # この上の変数群は基本、init以外のメソッドでは呼び出さない！

        self.board_start = [0 for _ in range(N*2)] + [self.ship] # ここ怪しい
        self.board_goal = [2 for _ in range(N*2)] + [2 - self.ship] # ここも怪しい
        self.open = [self.board_start]
        self.closed = []
        self.board_current = []

        self.condition = []

    def print_board(self):
        print(self.board_current)
    
    def set_condition(self):
        self.condition.append(lambda board: all(board[i] == board[self.N+i] or all(board[j] != board[self.N+i] for j in range(self.N)) for i in range(self.N)))
        # self.condition.append(lambda board: board in self.open)
        self.condition.append(lambda board: board not in self.closed)

    def forward(self):
        # openの最後の要素を取り出す！（深さ優先探索）
        self.board_current = self.open.pop() # エラーに注意！
        # openの最初の要素を取り出す！（広さ優先探索）
        # self.board_current = self.open.pop(0) # エラーに注意！
        if self.board_current in self.closed:
            return # 次のforward（つまり次の要素の取り出し）へ
        self.closed.append(self.board_current)

        # 探索中のノードの出力
        print(self.board_current)

        if self.board_current[self.N*2] == 0:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if value_1 == 0 and value_2 == 0:
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 2
                            new_board[self.N*2] = 2
                            if new_board == self.board_goal:
                                print(new_board)
                                print("Finished!")
                                return 1
                            elif all(check(new_board) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 2
                            new_board[j] = 2
                            new_board[self.N*2] = 2
                            if new_board == self.board_goal:
                                print(new_board)
                                print("Finished!")
                                return 1
                            elif all(check(new_board) for check in self.condition):
                                self.open.append(new_board)
                                # print(f"new: {new_board}")

        elif self.board_current[self.N*2] == 2:
  
            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if value_1 == 2 and value_2 == 2:
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 0
                            new_board[self.N*2] = 0
                            if new_board == self.board_goal:
                                print(new_board)
                                print("Finished!")
                                return 1
                            elif all(check(new_board) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 0
                            new_board[j] = 0
                            new_board[self.N*2] = 0
                            if new_board == self.board_goal:
                                print(new_board)
                                print("Finished!")
                                return 1
                            elif all(check(new_board) for check in self.condition):
                                self.open.append(new_board)
                                # print(f"new: {new_board}")

        return

    def search(self):
        self.set_condition()
        while self.open:
            res = self.forward()
            if res == 1:
              break


def main():
    newPuzzle = Puzzle(4)
    newPuzzle.search()


if __name__ == "__main__":
    main()
