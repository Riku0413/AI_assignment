import copy


class Puzzle:
    def __init__(self, N):
        self.N = N

        self.board_start = [0 for _ in range(N*2)] + [0, 1, 0, None] # 船の位置、f値、d値、親ノードのself.closed上のindex
        self.board_goal = [2 for _ in range(N*2)] + [2, 0, None, None] # 同上
        self.open = [self.board_start] # ここには長さ N × 2 + 4 のリストを格納
        self.closed = [] # 長さ N × 2 + 4 のリストを格納
        self.board_current = [] # 探索中のノードを保持

        self.condition = [] # 問題に応じた許される盤面の条件を格納
        self.route = [] # 見つけた正解ルート
        self.count = 0 # ノード探索数のカウント
    
    # たどることが許される盤面であるかどうかを判定する、問題に応じた条件の設定
    def set_condition(self):
        self.condition.append(lambda board: all(board[i] == board[self.N+i] or all(board[j] != board[self.N+i] for j in range(self.N)) for i in range(self.N)))
        self.condition.append(lambda board: all(board != sublist[:self.N*2+1] for sublist in self.closed))
    
    # 最終的に発見した解のルートを出力する
    def print_route(self, parent_index):
        # 答えの出力
        step = 2
        while parent_index:
            self.route.append(self.closed[parent_index])
            parent_index = self.closed[parent_index][self.N*2+3]
            step += 1
        print(self.board_start[:self.N*2+1])
        for board in reversed(self.route):
            print(board[:self.N*2+1])
        print(self.board_goal[:self.N*2+1])
        print("Goal!")
        print(f"The depth of goal: {step}\n")
        # 答えの出力 ここまで

    # 次の探索に備えてパラメータをリセットする
    def reset_parameter(self):
        self.open = [self.board_start] # ここには長さ N × 2 + 4 のリストを格納
        self.closed = [] # 長さ N × 2 + 4 のリストを格納
        self.board_current = [] # 探索中のノードを保持
        self.condition = [] # 問題に応じた許される盤面の条件を格納
        self.route = [] # 見つけた正解ルート
        self.count = 0 # ノード探索数のカウント

    # (3)において、ボートの左岸から右岸への直接移動を含んでいるかチェック
    def check_route(self, parent_index):
        
        while parent_index:
            self.route.append(self.closed[parent_index])
            parent_index = self.closed[parent_index][self.N*2+3]

        boat_positions = [0]
        for board in reversed(self.route):
            boat_positions.append(board[self.N*2])
        boat_positions.append(2)
        for i in range(1, len(boat_positions)):
            if abs(boat_positions[i] - boat_positions[i-1]) == 2:
                return True
        
        return False

    def forward(self, mode):
        if mode == "deep":
            self.board_current = self.open.pop()
        elif mode == "wide":
            self.board_current = self.open.pop(0)
        elif mode == "A":
            self.board_current = min(self.open, key=lambda lst: lst[-3])
            self.open.remove(self.board_current)
        else:
            return 0

        if any(self.board_current[:self.N*2+1] == sublist[:self.N*2+1] for sublist in self.closed):
            return # 次のforward（つまり次の要素の取り出し）へ
        parent_index = len(self.closed) # 追加
        self.closed.append(self.board_current) # 変更！

        # 探索中のノードの出力
        self.count += 1
        print(self.board_current[:self.N*2+1])

        # ボートが左岸にあるとき
        if self.board_current[self.N*2] == 0:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if value_1 == 0 and value_2 == 0:
                        if i > j:
                            continue
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 2
                            new_board[self.N*2] = 2
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                print(new_board[:self.N*2+1])
                                print("Finished!")
                                self.count += 1
                                print(f"the number of node searched: {self.count}")
                                self.print_route(parent_index)
                                return 1
                            elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 2
                            new_board[j] = 2
                            new_board[self.N*2] = 2
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                print(new_board[:self.N*2+1])
                                print("Finished!")
                                self.count += 1
                                print(f"the number of node searched: {self.count}")
                                self.print_route(parent_index)
                                return 1
                            elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
        
        # ボートが右岸にあるとき
        elif self.board_current[self.N*2] == 2:
        
            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if value_1 == 2 and value_2 == 2:
                        if i > j:
                            continue
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 0
                            new_board[self.N*2] = 0
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 0
                            new_board[j] = 0
                            new_board[self.N*2] = 0
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)

        return
    
    def calc_h(self, board):
        extracted_board = board
        # if extracted_board[self.N*2] == 0:
        #     h = max(extracted_board[:self.N*2].count(0) * 2 - 3, 1)
        # else:
        #     h = extracted_board[:self.N*2].count(0) * 2
        # return h
        h = 0
        left_list = [0 for _ in range(self.N)]
        center_list = [0 for _ in range(self.N)]
        right_list = [0 for _ in range(self.N)]
        for i in range(self.N):
            if extracted_board[i*2] == 0 and extracted_board[i*2+1] == 0:
                left_list[i] = 1
            elif extracted_board[i*2] == 1 and extracted_board[i*2+1] == 1:
                center_list[i] = 1                
            elif extracted_board[i*2] == 2 and extracted_board[i*2+1] == 2:
                right_list[i] = 1
        left_func = lambda x, i: x * 10**(self.N - 1 - i) # indexが小さい夫婦の位置を重視
        center_func = lambda x, i: x * 10**(self.N - 1 - i)
        right_func = lambda x, i: x * 10**(self.N - 1 - i) # indexが小さい夫婦の位置を重視
        for i in range(self.N):
            h += left_func(left_list[i], i) * 15
            # h -= 20/(left_func(left_list[i], i) + 1)
            h += 2/(right_func(right_list[i], i) + 1)
            h -= right_func(right_list[i], i) ** 3
            # h += 20/(center_func(center_list[i], i)+1)
        h -= board[-2]**10

        return h
    
    def search(self, mode):
        self.reset_parameter()
        self.set_condition()
        print(f"Started noraml game of {self.N} pair by \"{mode} search!\"")
        while self.open:
            res = self.forward(mode)
            if res == 0:
                print("Error")
                return
            if res == 1:
                return
        print("No resolution found.\n")
        return 

    def forward_island(self, mode):
        if mode == "deep":
            self.board_current = self.open.pop() # エラーに注意！
        elif mode == "wide":
            self.board_current = self.open.pop(0) # エラーに注意！  
        elif mode == "A":
            self.board_current = min(self.open, key=lambda lst: lst[-3])
            self.open.remove(self.board_current)
        else:
            return 0

        # if self.board_current[:self.N*2+1] in self.closed:
        if any(self.board_current[:self.N*2+1] == sublist[:self.N*2+1] for sublist in self.closed):
            return # 次のforward（つまり次の要素の取り出し）へ
        parent_index = len(self.closed) # 追加
        self.closed.append(self.board_current) # 変更！

        # 探索中のノードの出力
        self.count += 1
        print(self.board_current[:self.N*2+1])

        # ボートが左岸にあるとき
        if self.board_current[self.N*2] == 0:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 0 and value_2 == 0:
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 1 # 1人を左から真ん中へ
                            new_board[self.N*2] = 1 # ボートを左から真ん中へ
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 1
                            new_board[j] = 1
                            new_board[self.N*2] = 1
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
        
        # ボートが右岸にあるとき
        elif self.board_current[self.N*2] == 2:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 2 and value_2 == 2:
                        if i == j:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 1
                            new_board[self.N*2] = 1
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)
                        else:
                            new_board = copy.deepcopy(self.board_current)
                            new_board[i] = 1
                            new_board[j] = 1
                            new_board[self.N*2] = 1
                            new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                            new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                            new_board[self.N*2 + 3] = parent_index # 追加
                            if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                self.open.append(new_board)

        # ボートが真ん中の島にあるとき
        elif self.board_current[self.N*2] == 1:
  
            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 1 and value_2 == 1:
                        if i == j:
                            for k in range(2): # 右行きと左行き
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2*k
                                new_board[self.N*2] = 2*k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                    print(new_board[:self.N*2+1])
                                    print("Finished!")
                                    self.count += 1
                                    print(f"the number of node searched: {self.count}")
                                    self.print_route(parent_index)
                                    return 1
                                elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)
                        else:
                            for k in range(2): # 右行きと左行き
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2*k
                                new_board[j] = 2*k
                                new_board[self.N*2] = 2*k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                    print(new_board[:self.N*2+1])
                                    print("Finished!")
                                    self.count += 1
                                    print(f"the number of node searched: {self.count}")
                                    self.print_route(parent_index)
                                    return 1
                                elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)

        return

    def calc_h_island(self, board):
        # ver.1
        # return 0

        # ver.2
        # left_pair = 0
        # right_pair = 0
        # boat_position = board[self.N*2]
        # for i in range(self.N):
        #     if board[i*2] == 0 and board[i*2+1] == 0:
        #         left_pair += 1
        #     elif board[i*2] == 2 and board[i*2+1] == 2:
        #         right_pair += 1
        # # h = left_pair * 100
        # # h = 1000/(right_pair + 1)
        # # h = 1000/(right_pair + 1) + left_pair * 10
        # h = 1000/(right_pair + 1) + left_pair * 10 + boat_position * 5
        # return h

        h = 0
        left_list = [0 for _ in range(self.N)]
        right_list = [0 for _ in range(self.N)]
        for i in range(self.N):
            if board[i*2] == 0 and board[i*2+1] == 0:
                left_list[i] = 1      
            elif board[i*2] == 2 and board[i*2+1] == 2:
                right_list[i] = 1
        left_func = lambda x, i: x * 10**(self.N - 1 - i)
        right_func = lambda x, i: x * 10**(self.N - 1 - i)
        for i in range(self.N):
            h += left_func(left_list[i], i) * 15
            # h -= 20/(left_func(left_list[i], i) + 1)
            h += 2/(right_func(right_list[i], i) + 1)
            h -= right_func(right_list[i], i) ** 3
        h -= board[-2]**10
        return h

    def search_island(self, mode):
        self.reset_parameter()
        self.set_condition()
        print(f"Started island game of {self.N} pair by \"{mode} search!\"")
        while self.open:
            res = self.forward_island(mode)
            if res == 0:
                print("Error")
                return
            if res == 1:
                return
        print("No resolution found.\n")
        return 

    def forward_include_direct(self, mode):
        if mode == "deep":
            self.board_current = self.open.pop() # エラーに注意！
        elif mode == "wide":
            self.board_current = self.open.pop(0) # エラーに注意！  
        elif mode == "A":
            self.board_current = min(self.open, key=lambda lst: lst[-3])
            self.open.remove(self.board_current)
        else:
            return 0

        # if self.board_current[:self.N*2+1] in self.closed:
        if any(self.board_current[:self.N*2+1] == sublist[:self.N*2+1] for sublist in self.closed):
            return # 次のforward（つまり次の要素の取り出し）へ
        parent_index = len(self.closed) # 追加
        self.closed.append(self.board_current) # 変更！

        # 探索中のノードの出力
        self.count += 1
        print(self.board_current[:self.N*2+1])

        # ボートが左岸にあるとき
        if self.board_current[self.N*2] == 0:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 0 and value_2 == 0:
                        for k in range(2): # 真ん中島行きと、右岸行き
                            if i == j:
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2-k
                                new_board[self.N*2] = 2-k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)
                            else:
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2-k
                                new_board[j] = 2-k
                                new_board[self.N*2] = 2-k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)
        
        # ボートが右岸にあるとき
        elif self.board_current[self.N*2] == 2:

            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 2 and value_2 == 2:
                        for k in range(2): # 真ん中島行きと、左岸行き
                            if i == j:
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = k
                                new_board[self.N*2] = k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)
                            else:
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = k
                                new_board[j] = k
                                new_board[self.N*2] = k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)

        # ボートが真ん中の島にあるとき
        elif self.board_current[self.N*2] == 1:
  
            for i, value_1 in enumerate(self.board_current[:self.N * 2]):
                for j, value_2 in enumerate(self.board_current[:self.N * 2]):
                    if i > j:
                        continue
                    # print(i, j)
                    if value_1 == 1 and value_2 == 1:
                        if i == j:
                            for k in range(2): # 右行きと左行き
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2*k
                                new_board[self.N*2] = 2*k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                    if self.check_route(parent_index) != True:
                                        continue
                                    print(new_board[:self.N*2+1])
                                    print("Finished!")
                                    self.count += 1
                                    print(f"the number of node searched: {self.count}")
                                    self.print_route(parent_index)
                                    return 1
                                elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)
                        else:
                            for k in range(2): # 右行きと左行き
                                new_board = copy.deepcopy(self.board_current)
                                new_board[i] = 2*k
                                new_board[j] = 2*k
                                new_board[self.N*2] = 2*k
                                new_board[self.N*2 + 2] = self.board_current[self.N*2 + 2] + 1
                                new_board[self.N*2 + 1] = self.board_current[self.N*2 + 2] + 1 + self.calc_h_island(new_board)
                                new_board[self.N*2 + 3] = parent_index # 追加
                                if new_board[:self.N*2] == self.board_goal[:self.N*2]:
                                    if self.check_route(parent_index) != True:
                                        continue
                                    print(new_board[:self.N*2+1])
                                    print("Finished!")
                                    self.count += 1
                                    print(f"the number of node searched: {self.count}")
                                    self.print_route(parent_index)
                                    return 1
                                elif all(check(new_board[:self.N*2+1]) for check in self.condition):
                                    self.open.append(new_board)

        return

    def calc_h_include_direct(self, board):
        # return 0
        extracted_board = board
        h = 0
        left_list = [0 for _ in range(self.N)]
        right_list = [0 for _ in range(self.N)]
        for i in range(self.N):
            if extracted_board[i*2] == 0 and extracted_board[i*2+1] == 0:
                left_list[i] = 1    
            elif extracted_board[i*2] == 2 and extracted_board[i*2+1] == 2:
                right_list[i] = 1
        left_func = lambda x, i: x * 10**(self.N - 1 - i) # indexが小さい夫婦の位置を重視
        right_func = lambda x, i: x * 10**(self.N - 1 - i) # indexが小さい夫婦の位置を重視
        for i in range(self.N):
            h += left_func(left_list[i], i) * 15
            h += 2/(right_func(right_list[i], i) + 1)
            h -= right_func(right_list[i], i) ** 3
        h -= board[-2]**10

        return h
    
    def search_include_direct(self, mode):
        self.reset_parameter()
        self.set_condition()
        print(f"Started island game including direct boat move of {self.N} pair by \"{mode} search!\"")
        while self.open:
            res = self.forward_include_direct(mode)
            if res == 0:
                print("Error")
                return
            if res == 1:
                return
        print("No resolution found.\n")
        return 


def main():
    newPuzzle = Puzzle(4)
    # newPuzzle.search("deep")
    # newPuzzle.search("wide")
    # newPuzzle.search("A")
    # newPuzzle.search_island("deep")
    # newPuzzle.search_island("wide")
    newPuzzle.search_island("A")
    # newPuzzle.search_include_direct("A")


if __name__ == "__main__":
    main()
