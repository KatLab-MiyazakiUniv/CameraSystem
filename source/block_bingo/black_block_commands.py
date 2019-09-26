"""
    @file: black_block_commands.py
    @author: Takahiro55555
    @brief: 黒ブロック運搬経路をコマンドへ変換するクラス
"""
import math
import itertools
import unittest

from block_circles_path import BlockCirclesSolver, BlockCirclesCoordinate

class BlackBlockCommands():
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
        # インスタンス生成
        self.block_circles_solver = BlockCirclesSolver(bonus, black, color)
        self.block_circles_coordinate = BlockCirclesCoordinate()

        # 経路を計算
        route_tmp = self.block_circles_solver.solve()
        # 経路の軸の相違を吸収
        self.route = list(map(lambda x: (x[1], x[0]), route_tmp))

        """
        機体の向きの表現方法
        左上               右上
              0   1   2
            +---+---+--
          0 |   | → |    (1, 0)の機体 => (1, 0)
            +---+---+--
          1 | ↑ |   |    (0, 1)の機体 => (0, -1)
            +---+---+--
          2 |   |   |
        左下　　　　　　　　　右下
        """
        # 機体の向きを初期化
        self.direction = (1, 0)

        ### コマンドの初期化（定義） ###
        # HACK: 別ファイルから読み込んだほうが良いかも
        # ブロックビンゴエリアへの侵入
        self.ENTER_4 = 'a'
        self.ENTER_6 = 'b'
        # ブロックサークル間移動
        self.MOVE_CIRCLE = 'c'
        # 90度右回転
        self.TURN_RIGHT_90 = 'd'
        # 90度左回転
        self.TURN_LEFT_90 = 'e'
        # 180度回転
        self.TURN_180 = 'f'


    def gen_commands(self):
        """
        運搬経路からコマンドを生成する

        Returning
        ---------
        コマンドの文字列
        """
        commands = ""
        # 座標系の相違を吸収
        tmp_trans = (self.block_circles_coordinate.block_circles[4][1], self.block_circles_coordinate.block_circles[4][0])
        # ブロックビンゴエリアへの侵入先を決定
        if self.route[0] == tmp_trans:
            commands += self.ENTER_4
        else:
            commands += self.ENTER_6
        current_coordinate = self.route[0]
        for i in range(1, len(self.route)):
            commands += self.coordinate_to_command(current_coordinate, self.route[i], self.direction)
            current_coordinate = self.route[i]
        return commands


    def coordinate_to_command(self, robot_coor, next_coor, direction):
        """
        現在の座標と次の座標から動作を計算

        Parameters
        ----------
        robot_coor : tuple
            機体の座標
        next_coor : tuple
            次のの座標（隣の座標でないといけない）
        direction : tuple
            機体の向き
        
        Returning
        ---------
        tmp_commands : str
            一時コマンドの文字列
        """
        # 値のチェック
        if len(robot_coor) != 2:
            raise ValueError("robot_coor is invalid!")
        if len(next_coor) != 2:
            raise ValueError("next_coor is invalid!")
        if len(direction) != 2:
            raise ValueError("direction is invalid!")
        # 斜め移動や隣以外のブロックサークルへ移動するコマンドはコマンドは作成できない
        if abs(robot_coor[0] - next_coor[0]) + abs(robot_coor[1] - next_coor[1]) != 1:
            raise ValueError("Next coordinate value is in valid!")
        tmp_commands = ""
        # 機体の向きを設定
        next_direction = (next_coor[0] - robot_coor[0], next_coor[1] - robot_coor[1])
        tmp_commands += self.direction_to_command(direction, next_direction)
        # 機体の向きを更新
        self.direction = next_direction
        # ブロックサークル間移動
        tmp_commands += self.MOVE_CIRCLE
        return tmp_commands
    
    def direction_to_command(self, robot_direction, movement_direction):
        """
        機体の方向と進行方向からコマンドを計算

        Parameters
        ----------
        robot_direction : tuple
            機体の向き
        movement_direction : tuple
            移動方向
        
        Returning
        ---------
        command : str
        """
        # 値のチェック
        if len(robot_direction) != 2:
            raise ValueError("robot_direction is invalid!")
        if len(movement_direction) != 2:
            raise ValueError("movement_direction is invalid!")
        # 機体の向きと移動方向が一致している場合
        if robot_direction == movement_direction:
            return ""
        # 90度回転
        direction = self.detect_direction(robot_direction, movement_direction)
        if direction == "r":
            return self.TURN_RIGHT_90
        if direction == "l":
            return self.TURN_LEFT_90
        # 180度右回転
        if robot_direction[0] == movement_direction[0]:
            return self.TURN_180
        if robot_direction[1] == movement_direction[1]:
            return self.TURN_180
        return ""

    def detect_direction(self, robot_direction, movement_direction):
        """
        機体の向きから回転方向を判定する

        Parameters
        ----------
        robot_direction : tuple
            回転前の機体向き
        movement_direction : tuple
            回転後の機体の向き
        
        Returning
        ---------
        direction : str
            右に90度回転時 "r"
            左に90度回転時 "l"
            回転しない or 180度回転時 ""
        """
        # インデックスが増える方向に回転 => 右回転
        dx = (1, 0, -1, 0)
        dy = (0, 1, 0, -1)
        # 回転前のインデックスを取得
        for pre_index in range(len(dx)):
            tmp = (dx[pre_index], dy[pre_index])
            if robot_direction == tmp:
                break
        # 回転後のインデックスを取得
        for next_index in range(len(dx)):
            tmp = (dx[next_index], dy[next_index])
            if movement_direction == tmp:
                break
        # 右に90度回転
        if ((pre_index + 1) % 4) == next_index:
            return 'r'
        # 左に90度回転
        if ((next_index + 1) % 4) == pre_index:
            return 'l'
        # 回転しない or 180度回転
        return ''


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
            3. 末尾のコマンドは前進（サークル間移動）コマンドである
        """
        for bonus in range(1, 8 + 1):
            for black in range(1, 8 + 1):
                for color in range(1, 8 + 1):
                    # ブロックビンゴのルールによる制約
                    if bonus == black or black == color:
                        continue
                    generator = BlackBlockCommands(bonus, black, color)
                    commands = generator.gen_commands()
                    # 確認事項1.のテスト
                    self.assertTrue(commands[0] == generator.ENTER_4 or commands[0] == generator.ENTER_6)
                    flag = False
                    for comm in commands:
                        before_flag = flag
                        if comm == generator.TURN_180:
                            flag = True
                        elif comm == generator.TURN_LEFT_90:
                            flag = True
                        elif comm == generator.TURN_RIGHT_90:
                            flag = True
                        else:
                            flag = False
                        # 確認事項2.のテスト
                        self.assertTrue((before_flag != flag) or (not before_flag and not flag))
                    # 確認事項3.のテスト
                    self.assertTrue(commands[-1] == generator.MOVE_CIRCLE)

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
        generator = BlackBlockCommands(1, 2, 3)
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
                        self.assertEqual(commands, generator.MOVE_CIRCLE)
                    elif  ((pre_index + 1) % 4) == next_index:
                        # 確認事項5.のテスト
                        # 右90度
                        self.assertEqual(commands[0], generator.TURN_RIGHT_90)
                        self.assertEqual(commands[1], generator.MOVE_CIRCLE)
                    elif ((next_index + 1) % 4) == pre_index:
                        # 確認事項5.のテスト
                        # 左90度
                        self.assertEqual(commands[0], generator.TURN_LEFT_90)
                        self.assertEqual(commands[1], generator.MOVE_CIRCLE)
                    else:
                        # 確認事項5.のテスト
                        # 180度
                        self.assertEqual(commands[0], generator.TURN_180)
                        self.assertEqual(commands[1], generator.MOVE_CIRCLE)
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
        generator = BlackBlockCommands(1, 2, 3)
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
    #unittest.main()
    pass

if __name__ == "__main__":
    main()
	