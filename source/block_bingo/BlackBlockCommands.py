"""
    @file: black_block_commands.py
    @author: Takahiro55555
    @brief: 黒ブロック運搬経路をコマンドへ変換するクラス
"""
from BlockBingoCoordinate import BlockCirclesCoordinate
from BlockCirclesPath import BlockCirclesSolver


class BlackBlockCommands():
    def __init__(self, bonus, black, color, is_left=True):
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
        is_left : bool
            コース設定のためのフラグ
        """
        self.is_left = is_left

        # インスタンス生成
        self.block_circles_solver = BlockCirclesSolver(bonus, black, color, is_left)
        self.block_circles_coordinate = BlockCirclesCoordinate(is_left, bonus, color)

        # 経路を計算
        route_tmp = self.block_circles_solver.solve()
        # 経路の軸の相違を吸収
        self.reverse_route = route_tmp
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
        if self.is_left:
            self.direction = (1, 0)
        else:
            self.direction = (-1, 0)

        ### コマンドの初期化（定義） ###
        # HACK: 別ファイルから読み込んだほうが良いかも
        # ブロックビンゴエリアへの侵入
        self.ENTER_4 = 'a'  # Lコース
        self.ENTER_6 = 'b'  # Lコース
        self.ENTER_5 = 'w'  # Rコース
        self.ENTER_8 = 'x'  # Rコース
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
        # ブロックビンゴエリアへの侵入先を決定
        if self.is_left:
            tmp_trans = list(self.block_circles_coordinate.get(4))
            # 座標系の相違を吸収
            tmp_trans[0], tmp_trans[1] = tmp_trans[1], tmp_trans[0]
            if self.route[0] == tmp_trans:
                commands += self.ENTER_4
            else:
                commands += self.ENTER_6
        else:
            tmp_trans = list(self.block_circles_coordinate.get(5))
            # 座標系の相違を吸収
            tmp_trans[0], tmp_trans[1] = tmp_trans[1], tmp_trans[0]
            if self.route[0] == tmp_trans:
                commands += self.ENTER_5
            else:
                commands += self.ENTER_8
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


def main():
    pass


if __name__ == "__main__":
    main()
