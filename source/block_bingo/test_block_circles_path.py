from BlockCirclesPath import BlockCirclesSolver
from BlockCirclesPath import BlockCirclesTracks
import unittest

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
                solver = BlockCirclesSolver(bonus, black, 4, True)
                self.assertEqual((2, 0), solver.enter_block_circle())
        
        # 確認事項2.のテスト
        for bonus in range(1, 8 + 1):
            for color in range(1, 8 + 1):
                if bonus == 6 or color == 6:
                    continue
                solver = BlockCirclesSolver(bonus, 6, color, True)
                self.assertEqual((2, 0), solver.enter_block_circle())
        
        # 確認事項3.のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        # 例外的な2条件を省くための制約
                        if color == 4 or black == 6:
                            continue
                        solver = BlockCirclesSolver(bonus, black, color, True)
                        self.assertEqual((1, 0), solver.enter_block_circle())

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
                solver = BlockCirclesSolver(bonus, black, 5, False)
                self.assertEqual((2, 2), solver.enter_block_circle())
        
        # 確認事項2. のテスト
        for bonus in range(1, 8 + 1):
            for color in range(1, 8 + 1):
                if bonus == 8 or color == 8:
                    continue
                solver = BlockCirclesSolver(bonus, 8, color, False)
                self.assertEqual((2, 2), solver.enter_block_circle())
        
        # 確認事項3. のテスト
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        # 例外的な2条件を省くための制約
                        if color == 5 or black == 8:
                            continue
                        solver = BlockCirclesSolver(bonus, black, color, False)
                        self.assertEqual((1, 2), solver.enter_block_circle())


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
                    solver = BlockCirclesSolver(bonus, black, color, True)
                    enter = solver.enter_block_circle()
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
                    solver = BlockCirclesSolver(bonus, black, color, True)
                    path = solver.path_to_bonus_circle(BlockCirclesTracks(solver.coordinate))
                    # 確認事項1.のテスト
                    self.assertTrue(solver.coordinate.get(black) not in path)
                    # 確認事項2.のテスト
                    self.assertTrue(solver.coordinate.get(color) not in path[0:-1])

    def solve(self, is_left):
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
                    solver = BlockCirclesSolver(bonus, black, color, is_left)
                    enter = solver.enter_block_circle()
                    path = solver.solve()
                    # 確認事項1.のテスト
                    self.assertEqual(enter, path[0])
                    # 確認事項2.のテスト
                    self.assertEqual(solver.coordinate.get(bonus), path[-1])
                    # 確認事項3.のテスト
                    self.assertTrue(solver.coordinate.get(color) not in path[0:-1])

    def test_solve_left(self):
        self.solve(True)

    def test_solve_right(self):
        self.solve(False)

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
        solver = BlockCirclesSolver(0, 1, 2, True) # 引数の値は適当
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
    unittest.main()