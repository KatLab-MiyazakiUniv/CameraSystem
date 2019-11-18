"""
    @file: test_black_block_commands.py
    @author: Takahiro55555
    @brief: 黒ブロック運搬経路をコマンドへ変換するクラスのテスト
"""

import math
import itertools
import unittest

from BlackBlockCommands import BlackBlockCommands
from commands import Instructions

class BlackBlockCommandsTest(unittest.TestCase):
    """
    BlackBlockCommandsのテストクラス
    """
    def test_gen_commands(self):
        """
        gen_commands()のテストコード
        確認事項
            1. 先頭のコマンドはブロックサークルへ侵入するコマンドである
            2. 回転コマンドが連続することはない
            3. 末尾のコマンドはブロック設置コマンドである
        """
        # ブロック配置の組み合わせを列挙
        block_products = tuple(itertools.product((1, 2, 3, 4, 5, 6, 7, 8), repeat=3))
        for is_left in [True, False]:
            for product in block_products:
                bonus, color, black = product
                # ブロックビンゴのルールによる制約
                if bonus == black or black == color:
                    continue
                generator = BlackBlockCommands(bonus, black, color, is_left=is_left)
                commands = generator.gen_commands()
                # 確認事項1.のテスト
                if is_left:
                    self.assertTrue(commands[0] == Instructions.ENTER_BINGO_AREA_L4 or commands[0] == Instructions.ENTER_BINGO_AREA_L6)
                else:
                    self.assertTrue(commands[0] == Instructions.ENTER_BINGO_AREA_R5 or commands[0] == Instructions.ENTER_BINGO_AREA_R8)

                flag = False
                for comm in commands:
                    before_flag = flag
                    if comm == Instructions.SPIN180:
                        flag = True
                    elif comm == Instructions.SPIN_LEFT:
                        flag = True
                    elif comm == Instructions.SPIN_RIGHT:
                        flag = True
                    else:
                        flag = False
                    # 確認事項2.のテスト
                    self.assertTrue((before_flag != flag) or (not before_flag and not flag))
                # 確認事項3.のテスト
                self.assertTrue(commands[-1] == Instructions.PUT)

    def test_coordinate_to_command(self):
        """
        coordinate_to_command()のテストコード
        確認事項
            1. ブロックサークルの斜め移動はできないため、エラーを返す
            2. ブロックサークルをまたぐ移動はできないため、エラーを返す
            3. 各引数は要素数2のタプル又はリスト
            4. 機体の向きが進行方向と同じ場合、直進（サークル間移動)する
            5. 移動方向と機体の向きが異なる場合、所定の角度回転したのち直進（サークル間移動）する
        """
        # インデックスが増える方向に回転 => 右回転
        dx = (1, 0, -1, 0)
        dy = (0, 1, 0, -1)
        generator = BlackBlockCommands(1, 2, 3, True)
        next_coor = (0, 0)
        # 座標の組み合わせを列挙
        movement_coordinates = tuple(itertools.product(tuple(itertools.product((0, 1, 2), repeat=2)), repeat=2))
        for coordinates in movement_coordinates:
                pre_coor, next_coor = coordinates
                distance = math.sqrt((pre_coor[0] - next_coor[0])**2 + (pre_coor[1] - next_coor[1])**2)
                if distance == 0:
                    # 移動しないことは無い
                    continue
                elif distance != 1:
                    with self.assertRaises(ValueError):
                        # 確認事項1.確認事項2.の確認
                        generator.coordinate_to_command(pre_coor, next_coor, (1, 0))
                    continue
                next_direction = (next_coor[0]-pre_coor[0], next_coor[1]-pre_coor[1])
                # 回転後のインデックスを取得
                for next_index in range(4):
                    tmp = (dx[next_index], dy[next_index])
                    if next_direction == tmp:
                        break
                for pre_index in range(4):
                    robot_direction = (dx[pre_index], dy[pre_index])
                    generator.direction = robot_direction
                    commands = generator.coordinate_to_command(pre_coor, next_coor, robot_direction)
                    if pre_index == next_index:
                        # 確認事項4.のテスト
                        self.assertEqual(commands, Instructions.STRAIGHT)
                    elif  ((pre_index + 1) % 4) == next_index:
                        # 確認事項5.のテスト
                        # 右90度
                        self.assertEqual(commands[0], Instructions.SPIN_RIGHT)
                        self.assertEqual(commands[1], Instructions.STRAIGHT)
                    elif ((next_index + 1) % 4) == pre_index:
                        # 確認事項5.のテスト
                        # 左90度
                        self.assertEqual(commands[0], Instructions.SPIN_LEFT)
                        self.assertEqual(commands[1], Instructions.STRAIGHT)
                    else:
                        # 確認事項5.のテスト
                        # 180度
                        self.assertEqual(commands[0], Instructions.SPIN180)
                        self.assertEqual(commands[1], Instructions.STRAIGHT)
        # 確認事項3.のテスト
        with self.assertRaises(TypeError):
            generator.coordinate_to_command(1, 1, 1)
        with self.assertRaises(TypeError):
            generator.coordinate_to_command((1, 1), 1, 1)
        with self.assertRaises(TypeError):
            generator.coordinate_to_command((1, 1), (1, 0), 1)

    def test_direction_to_command(self):
        """
        direction_to_command()のテストコード
        確認事項
            1. 左右90度に回転する際、文字列'r'又は'l'を返すこと
            2. 左右180度回転する際、空文字列''を返すこと
            3. 回転しない際、空文字列''を返すこと
            4. 上記の条件を満たさない際、空文字列''を返すこと
        """
        generator = BlackBlockCommands(1, 2, 3, True)
        dx = (1, 0, -1, 0)
        dy = (0, 1, 0, -1)
        # 確認事項1.のテスト
        for pre_index in range(4):
            next_index = (pre_index + 1) % 4
            pre_dir = (dx[pre_index], dy[pre_index])
            next_dir = (dx[next_index], dy[next_index])
            self.assertEqual('r', generator.detect_direction(pre_dir, next_dir))
            self.assertEqual('l', generator.detect_direction(next_dir, pre_dir))
        # 確認事項2.のテスト
        for pre_index in range(4):
            next_index = (pre_index + 2) % 4
            pre_dir = (dx[pre_index], dy[pre_index])
            next_dir = (dx[next_index], dy[next_index])
            self.assertEqual('', generator.detect_direction(pre_dir, next_dir))
            self.assertEqual('', generator.detect_direction(next_dir, pre_dir))
        # 確認事項3.のテスト
        for i in range(4):
            dirction = (dx[i], dy[i])
            self.assertEqual('', generator.detect_direction(dirction, dirction))
        # 確認事項4.のテスト
        self.assertEqual('', generator.detect_direction((1, 2), (3, 4)))

def main():
    unittest.main()

if __name__ == "__main__":
    main()