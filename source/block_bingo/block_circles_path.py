"""
    @file: block_circles_path.py
    @author: T.Miyaji
    @brief: ブロックサークル内の黒ブロックを運搬する経路計算クラス
"""
import unittest

class BlockCirclesCoordinate():
    def __init__(self):
        """
        1 ~ 8までのサークル番号を辞書に格納する。
        """
        self.block_circles = { 1: (0, 0), 2: (0, 1), 3: (0, 2),
                               4: (1, 0),            5: (1, 2),
                               6: (2, 0), 7: (2, 1), 8: (2, 2)}
    
    def get(self, circle_number):
        """
        ブロックサークル番号に関連するサークルの座標を返す。
        
        Parameters
        ----------
        circle_number : int
            ブロックサークル番号
        """
        if circle_number <= 0 or 8 < circle_number:
            raise ValueError('Block circle number is invalid!')
        return self.block_circles[circle_number]

class BlockCirclesTracks():
    def __init__(self, coordinate):
        """
        ブロックサークル間を移動する際の経路を格納する
        
        Parameters
        ----------
        coordinate : BlockCirclesCoordinate
            ブロックサークル番号に関連するサークルの座標
        """
        
        # 内回りの経路
        self.inner_tracks = [coordinate.get(1), coordinate.get(4),
                             coordinate.get(6), coordinate.get(7),
                             coordinate.get(8), coordinate.get(5),
                             coordinate.get(3), coordinate.get(2)]
        # 外回りの経路
        self.outer_tracks = [coordinate.get(1), coordinate.get(2),
                             coordinate.get(3), coordinate.get(5), 
                             coordinate.get(8), coordinate.get(7),
                             coordinate.get(6), coordinate.get(4)]

class BlockCirclesSolver():
    def __init__(self, bonus, black, color):
        """
        ブロックサークル内の黒ブロックを運搬する経路を計算するための情報を登録する。
        
        Parameters
        ----------
        bonus : int
            ボーナスサークル番号
        black : int
            ブロックサークル内の黒ブロックが置かれているサークル番号
        color : int
            ブロックサークル内のカラーブロックが置かれているサークル番号
        """
        self.bonus = bonus
        self.black = black
        self.color = color
        self.coordinate = BlockCirclesCoordinate()
    
    def solve(self, is_left = True):
        """
        ブロックサークル内の黒ブロック運搬経路を計算する。
        
        Parameters
        ----------
        is_left : bool
            LコースならばTrue, RコースならばFalse
        """
        tracks = BlockCirclesTracks(self.coordinate)
        
        # ブロックサークルに進入するサークル番号を計算する
        enter = self.enter_block_circle(is_left)
        
        # 黒ブロックを取得するための経路を計算する
        catch_path = self.path_to_catch_block(enter, tracks)
        
        # 黒ブロックが置かれたサークルからボーナスサークルまでの経路を計算する
        placement_path = self.path_to_bonus_circle(tracks)
        
        return [enter] + catch_path + placement_path
            
    def subset_of_tracks(self, start, goal, tracks):
        """
        経路の部分集合を取得する。
        
        Parameters
        ----------
        start : tuple
            始点となるサークルの座標
        goal : tuple
            終点となるサークルの座標
        tracks : list
            経路
        """
        # 始点または終点が経路に存在しない場合は、Noneを返す
        if start not in tracks or goal not in tracks:
            return None

        # 始点は部分集合に含めないために1を足す        
        start_index = tracks.index(start) + 1
        # 終点は部分集合に含めるために1を足す
        goal_index = tracks.index(goal) + 1
        
        # 始点が終点よりも後ろにある場合、始点と経路の末尾、経路の先頭と終点までの部分集合を連結して返す(循環リスト)
        if goal_index < start_index:
            # 始点と経路の末尾までの部分集合を取得する
            back = tracks[start_index : len(tracks)]
            # 経路の先頭と終点までの部分集合を取得する
            front = tracks[0 : goal_index]
            return back + front
            
        return tracks[(start_index) % len(tracks) : goal_index]
    
    def enter_block_circle(self, is_left):
        """
        ブロックサークルに進入するサークル番号を計算する。
        
        Parameters
        ----------
        is_left : bool
            LコースならばTrue, RコースならばFalse
        """
        # 原則としてLコースのときは、4番サークルに進入する (Rコースのときは、5番サークル)
        enter = self.coordinate.get(4) if is_left else self.coordinate.get(5)
        # 代替策としてLコースのときは、6番サークルに進入する (Rコースのときは、8番サークル)
        plan_b = self.coordinate.get(6) if is_left else self.coordinate.get(8)
        
        # 進入サークルにカラーブロックが置いてあるかチェックする
        if enter == self.coordinate.get(self.color):
            enter = plan_b
        
        # 代替策のサークルに黒ブロックが置いてあるかチェックする
        if plan_b == self.coordinate.get(self.black):
            enter = plan_b
        
        return enter

    def path_to_catch_block(self, enter, tracks):
        """
        黒ブロックを取得するための経路を計算する。
        
        Parameters
        ----------
        enter : tuple
            進入するサークルの座標
        tracks : list
            経路
        """
        # 原則として内回りの経路を選択する
        path = self.subset_of_tracks(enter, self.coordinate.get(self.black), tracks.inner_tracks)
        
        # 選択した経路内にカラーブロックが置かれているサークルがあるかチェックする
        if self.coordinate.get(self.color) in path:
            path = self.subset_of_tracks(enter, self.coordinate.get(self.black), tracks.outer_tracks)
        
        return path

    def path_to_bonus_circle(self, tracks):
        """
        黒ブロックが置かれたサークルからボーナスサークルまでの経路を計算する。
        
        Parameters
        ----------
        tracks : list
            経路
        """
        # 原則として内回りの経路を選択する
        path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.inner_tracks)
        outer_path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.outer_tracks)
        
        # 選択した経路内にカラーブロックが置かれているサークルがあるかチェックする
        if self.coordinate.get(self.color) in path[0:-1]:
            path = self.subset_of_tracks(self.coordinate.get(self.black), self.coordinate.get(self.bonus), tracks.outer_tracks)
        # 内回り、外回りの両方にもゴールを除いてカラーブロックが置かれていないとき
        elif self.coordinate.get(self.color) not in outer_path[0:-1]:
            # 内回りよりも外回りの方が早い場合は、外回りを採用する
            path = outer_path if len(outer_path) < len(path) else path
        return path

def left_course():
    """
    Lコース版のテストコード
    """
    bonus = 5
    black = 3
    color = 5

    solver = BlockCirclesSolver(bonus, black, color)
    # solve関数を呼び出して運搬経路を計算させる(デフォルトでLeftコースの場合になる)
    path = solver.solve()
    print(path)

def right_course():
    """
    Rコース版のテストコード
    """
    bonus = 4
    black = 8
    color = 6

    solver = BlockCirclesSolver(bonus, black, color)
    # solve関数を呼び出して運搬経路を計算させる(Rightコースの場合)
    path = solver.solve(False)
    print(path)
class BlockCirclesSolverTest(unittest.TestCase):
    """
    BlockCirclesSolverのテストクラス
    """
    def test_enter_block_circle(self):
        """
        enter_block_circle()のテストコード
        確認事項
            1. 4番サークルにカラーブロックが置かれている場合、6番に進入すること
            2. 6番サークルに黒ブロックが置かれている場合、6番に進入すること
            3. 上記2条件に当てはまらない場合、4番に進入すること
        """
        # 確認事項1.のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                if black == 4 or bonus == black:
                    continue
                solver = BlockCirclesSolver(bonus, black, 4)
                self.assertEqual((2, 0), solver.enter_block_circle(True))
        
        # 確認事項2.のテスト
        for bonus in range(1, 8 + 1):
            for color in range(1, 8 + 1):
                if bonus == 6 or color == 6:
                    continue
                solver = BlockCirclesSolver(bonus, 6, color)
                self.assertEqual((2, 0), solver.enter_block_circle(True))
        
        # 確認事項3.のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        # 例外的な2条件を省くための制約
                        if color == 4 or black == 6:
                            continue
                        solver = BlockCirclesSolver(bonus, black, color)
                        self.assertEqual((1, 0), solver.enter_block_circle(True))

    def test_enter_block_circle_right(self):
        """
        enter_block_circle()のテストコード Rコース版
        確認事項
            1. 5番サークルにカラーブロックが置かれている場合、8番に進入すること
            2. 8番サークルに黒ブロックが置かれている場合、8番に進入すること
            3. 上記2条件に当てはまらない場合、5番に進入すること
        """
        # 確認事項1. のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                if black == 5 or bonus == black:
                    continue
                solver = BlockCirclesSolver(bonus, black, 5)
                self.assertEqual((2, 2), solver.enter_block_circle(False))
        
        # 確認事項2. のテスト
        for bonus in range(1, 8 + 1):
            for color in range(1, 8 + 1):
                if bonus == 8 or color == 8:
                    continue
                solver = BlockCirclesSolver(bonus, 8, color)
                self.assertEqual((2, 2), solver.enter_block_circle(False))
        
        # 確認事項3. のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        # 例外的な2条件を省くための制約
                        if color == 5 or black == 8:
                            continue
                        solver = BlockCirclesSolver(bonus, black, color)
                        self.assertEqual((1, 2), solver.enter_block_circle(False))


    def test_path_to_catch_block(self):
        """
        path_to_catch_block()のテストコード
        確認事項
            1. 求めた経路内にカラーブロックが置かれたサークルは存在しないこと
            2. 求めた経路内に進入サークルは含まれていないこと
        """
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        continue
                    solver = BlockCirclesSolver(bonus, black, color)
                    enter = solver.enter_block_circle(True)
                    path = solver.path_to_catch_block(enter, BlockCirclesTracks(solver.coordinate))
                    # 確認事項1.のテスト
                    self.assertTrue(solver.coordinate.get(color) not in path)
                    # 確認事項2.のテスト
                    self.assertTrue(enter not in path)

    def test_path_to_bonus_circle(self):
        """
        path_to_bonus_circle()のテストコード
        確認事項
            1. 求めた経路内に黒ブロックが置かれたサークルは存在しないこと
            2. 求めた経路の末尾を除いて、カラーブロックが置かれたサークルは存在しないこと
        """
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        continue
                    solver = BlockCirclesSolver(bonus, black, color)
                    path = solver.path_to_bonus_circle(BlockCirclesTracks(solver.coordinate))
                    # 確認事項1.のテスト
                    self.assertTrue(solver.coordinate.get(black) not in path)
                    # 確認事項2.のテスト
                    self.assertTrue(solver.coordinate.get(color) not in path[0:-1])

    def test_solve(self):
        """
        solve()のテストコード
        確認事項
            1. 求めた経路の先頭は、進入サークルの座標になっていること
            2. 求めた経路の末尾は、ボーナスサークルの座標になっていること
            3. 求めた経路の末尾を除いて、カラーブロックが置かれたサークルは存在しないこと
        """
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        continue
                    solver = BlockCirclesSolver(bonus, black, color)
                    enter = solver.enter_block_circle(True)
                    path = solver.solve()
                    # 確認事項1.のテスト
                    self.assertEqual(enter, path[0])
                    # 確認事項2.のテスト
                    self.assertEqual(solver.coordinate.get(bonus), path[-1])
                    # 確認事項3.のテスト
                    self.assertTrue(solver.coordinate.get(color) not in path[0:-1])

    def test_subset_of_tracks(self):
        """
        subset_of_tracks()のテストコード
        確認事項
            1. リストに含まれない要素が指定されたときはNoneを返すこと
            2. 部分集合の先頭は、始点を含まないこと
            3. 部分集合の末尾は、終点を含むこと
            4. 始点が終点よりも大きい場合の部分集合は、元のリストから(終点→始点の場合の部分集合)を引いた差集合になっていること
            5. 4.の条件を除いて部分集合は、元のリストの順序を保った状態の部分集合となっていること
        """
        original = [i + 1 for i in range(0, 5)] # [1, 2, 3, 4, 5]
        solver = BlockCirclesSolver(0, 1, 2) # 引数の値は適当
        # 確認事項1.のテスト
        self.assertIsNone(solver.subset_of_tracks(0, 3, original))
        self.assertIsNone(solver.subset_of_tracks(2, 6, original))
        # 確認事項2.のテスト
        self.assertTrue(1 not in solver.subset_of_tracks(1, 3, original))
        # 確認事項3.のテスト
        self.assertTrue(3 in solver.subset_of_tracks(1, 3, original))
        # 確認事項4.のテスト
        subtrahend = solver.subset_of_tracks(2, 4, original) # [3, 4]
        subset = solver.subset_of_tracks(4, 2, original) # [5, 1, 2]
        self.assertEqual(set(original) - set(subtrahend), set(subset))
        # 確認事項5.のテスト
        start = original.index(2) + 1
        goal = original.index(5) + 1
        self.assertEqual(original[start:goal], solver.subset_of_tracks(2, 5, original))

if __name__ == '__main__':
    #unittest.main()
    left_course()
    right_course()