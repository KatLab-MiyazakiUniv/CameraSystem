"""
    @file: black_block_commands.py
    @author: Takahiro55555
    @brief: 黒ブロック運搬経路をコマンドへ変換するクラス
"""
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
        self.route = self.block_circles_solver.solve()

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
        # ブロックビンゴエリアへの侵入
        self.ENTER_4 = '4'
        self.ENTER_6 = '6'
        # ブロックサークル間移動
        self.MOVE_CIRCLE = 'm'
        # 90度右回転
        self.TURN_RIGHT_90 = 'r'
        # 90度左回転
        self.TURN_LEFT_90 = 'l'
        # 180度回転
        self.TURN_180 = 'v'


    def gen_commands(self):
        """
        運搬経路からコマンドを生成する

        Returning
        ---------
        コマンドの文字列
        """
        commands = ""
        # ブロックビンゴエリアへの侵入先を決定
        if self.route[0] == self.block_circles_coordinate.block_circles[4]:
            commands += self.ENTER_4
        else:
            commands += self.ENTER_6
        
        current_coordinate = self.route[0]
        for i in range(1, len(self.route)):
            commands += self.coordinate_to_command(current_coordinate, self.route[i], self.direction)
            current_coordinate = self.route[i]
        return commands


    def coordinate_to_command(self, current_coor, next_coor, direction):
        """
        現在の座標と次の座標から動作を計算

        Parameters
        ----------
        current_coor : tuple
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
        if len(current_coor) != 2:
            raise ValueError("current_coor is invalid!")
        if len(next_coor) != 2:
            raise ValueError("next_coor is invalid!")
        if len(direction) != 2:
            raise ValueError("direction is invalid!")
        # 斜め移動や隣以外のブロックサークルへ移動するコマンドはコマンドは作成できない
        if abs(current_coor[0] - next_coor[0]) + abs(current_coor[1] - next_coor[1]) != 1:
            raise ValueError("Next coordinate value is in valid!")

        tmp_commands = ""
        # 機体の向きを設定
        if current_coor[0] == next_coor[0]:
            # 横方向の移動
            if current_coor[1] < next_coor[1]:
                # 右へ移動
                next_direction = (1, 0)
                tmp_commands += self.direction_to_command(self.direction, next_direction)
            else:
                # 左へ移動
                next_direction = (-1, 0)
                tmp_commands += self.direction_to_command(self.direction, next_direction)
        elif current_coor[1] == next_coor[1]:
            # 縦方向の移動
            if current_coor[0] < next_coor[0]:
                # 下へ移動
                next_direction = (0, 1)
                tmp_commands += self.direction_to_command(self.direction, next_direction)
            else:
                # 上へ移動
                next_direction = (0, -1)
                tmp_commands += self.direction_to_command(self.direction, next_direction)

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
        None
        """
        # 値のチェック
        if len(robot_direction) != 2:
            raise ValueError("robot_direction is invalid!")
        if len(movement_direction) != 2:
            raise ValueError("movement_direction is invalid!")

        # 機体の向きと移動方向が一致している場合
        if robot_direction == movement_direction:
            return ""
        # 180度右回転
        if robot_direction[0] == movement_direction[0]:
            return self.TURN_180
        if robot_direction[1] == movement_direction[1]:
            return self.TURN_180
        # 90度回転
        direction = self.detect_direction(robot_direction, movement_direction)
        if direction == "r":
            return self.TURN_RIGHT_90
        if direction == "l":
            return self.TURN_LEFT_90
    

    def detect_direction(self, pre_direction, next_direction):
        """
        機体の向きから回転方向を判定する

        Parameters
        ----------
        pre_direction : tuple
            回転前の機体向き
        next_direction : tuple
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
            if pre_direction == tmp:
                break
        # 回転後のインデックスを取得
        for next_index in range(len(dx)):
            tmp = (dx[next_index], dy[next_index])
            if next_direction == tmp:
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
        pass
    
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
        pass
    
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
        for pre_i in range(4):
            next_i = (pre_i + 1) % 4
            pre_dir = (dx[pre_i], dy[pre_i])
            next_dir = (dx[next_i], dy[next_i])
            self.assertEqual('r', generator.detect_direction(pre_dir, next_dir))
            self.assertEqual('l', generator.detect_direction(next_dir, pre_dir))
        # 確認事項2.のテスト
        for pre_i in range(4):
            next_i = (pre_i + 2) % 4
            pre_dir = (dx[pre_i], dy[pre_i])
            next_dir = (dx[next_i], dy[next_i])
            self.assertEqual('', generator.detect_direction(pre_dir, next_dir))
            self.assertEqual('', generator.detect_direction(next_dir, pre_dir))
        # 確認事項3.のテスト
        for i in range(4):
            dirction = (dx[i], dy[i])
            self.assertEqual('', generator.detect_direction(dirction, dirction))
        # 確認事項4.のテスト
        self.assertEqual('', generator.detect_direction((1, 2), (3, 4)))

def main():
    #test = BlackBlockCommandsTest()
    unittest.main()

if __name__ == "__main__":
    main()
	