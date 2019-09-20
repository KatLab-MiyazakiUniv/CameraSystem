"""
    @file: black_block_commands.py
    @author: Takahiro55555
    @brief: 黒ブロック運搬経路をコマンドへ変換するクラス
"""
import unittest

from block_circles_path import BlockCirclesSolver

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
        # 経路を計算
        self.route = self.block_circles_solver.solve()

        """
        機体の向きの表現方法
              0   1   2
            +---+---+--
          0 |   | → |    (1, 0)の機体 => (1, 0)
            +---+---+--
          1 | ↑ |   |    (0, 1)の機体 => (0, -1)
            +---+---+--
          2 |   |   |
        """
        # 機体の向きを初期化
        self.direction = (1, 0)

        ### コマンドの初期化（定義） ###
        # ブロックビンゴエリアへの侵入
        self.__ENTER = 'a'
        # ブロックサークル間移動
        self.__MOVE_CIRCLE = 'b'
        # 90度右回転
        self.__TURN_RIGHT_90 = 'c'
        # 90度左回転
        self.__TURN_LEFT_90 = 'd'
        # 180度回転
        self.__TURN_180 = 'e'


    def route_to_commands(self):
        """
        運搬経路からコマンドを生成する
        """
        pass

    def coordinate_to_command(self, current, next, direction):
        """
        現在の座標と次の座標から動作を計算

        Parameters
        ----------
        current : tuple
            現在の機体の座標
        next : tuple
            次の機体の座標
        direction : tuple
            現在の機体の向き
        """
        pass

def main():
    commands_generator = BlackBlockCommands(1, 2, 3)
    print(commands_generator.route)

if __name__ == "__main__":
    main()
