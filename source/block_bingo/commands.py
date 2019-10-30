"""
    @file   commands.py
    @author T.Miyaji
    @brief  ブロックビンゴ攻略のための運搬経路を走行体動作コマンドに変換する。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

class Instructions():
    ENTER_BINGO_AREA_L4 = 'a'
    ENTER_BINGO_AREA_L6 = 'b'
    STRAIGHT = 'c'
    SPIN_RIGHT = 'd'
    SPIN_LEFT = 'e'
    SPIN180 = 'f'
    PUT = 'g'

    MOVE_NODE = 'u'


    def translate(self, instruction):
        ja = {Instructions.ENTER_BINGO_AREA_L4: '4番サークルに進入',
              Instructions.ENTER_BINGO_AREA_L6: '6番サークルに進入',
              Instructions.STRAIGHT: 'ブロックサークル間を直進',
              Instructions.SPIN_RIGHT: '右に90°回頭する',
              Instructions.SPIN_LEFT: '左に90°回頭する',
              Instructions.SPIN180: '180°回頭する',
              Instructions.PUT: 'ブロックを黒線の中点から設置',
        
              Instructions.MOVE_NODE: '交点サークルから黒線の中点まで直進'
        }
        return ja[instruction]


class Commands():
    def __init__(self, block_circles, cross_circles):
        """
        ブロックサークルおよび交点サークルの情報を登録する。

        Parameters
        ----------
        block_circles : BlockCirclesCoordinate
            ブロックサークルの座標
        cross_circles : CrossCirclesCoordinate
            交点サークルの座標
        """
        self.block_circles = block_circles
        self.cross_circles = cross_circles

        # コマンドのリスト
        self.commands = []
    
    
    def convert(self, src, dst, direction, path):
        """
        運搬経路をコマンド変換する。

        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        direction : int
            方角: 上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
          6   2
            4
        path : list
            運搬経路（移動する座標のリスト）
        """
        # 始点にブロックが置いてあるか調べる。
        has_block = src in self.cross_circles.open
        # srcの前に運搬経路が存在しないことを確認する。
        if src == path[0]:
            self.spin(src, dst, direction, has_block)
    

    def get(self):
        return self.commands


    def get_next_direction(self, src, dst):
        """
        始点から終点までの移動したときの走行体の向きを取得する。
        方角: 上向きを0とし、時計回りに45度=1、90度=2、135度=3・・・315度=7とする
            0
          6   2
            4
        Parameters
        ----------
        src : tuple
            始点の座標
        dst : tuple
            終点の座標
        """
        subtraction = (dst[0]-src[0], dst[1]-src[1])

        if subtraction == (-1, 0) or subtraction == (-0.5, 0):
            return 0    # 北向き
        if subtraction == (0, 1) or subtraction == (0, 0.5):
            return 2    # 東向き
        if subtraction == (1, 0) or subtraction == (0.5, 0):
            return 4    # 南向き
        if subtraction == (0, -1) or subtraction == (0, -0.5):
            return 6    # 西向き
        raise ValueError('could not calculate direction')


    def spin(self, src, dst, direction, has_block):
        """
        回頭コマンドへ変換する。
        """
        next_direction = self.get_next_direction(src, dst)
        
        # 次の方向と現在の方向を引き算する。
        sub = next_direction - direction

        if sub == 2 or sub == 6:
            self.commands.append(Instructions.SPIN_RIGHT)
            return next_direction
        if sub == 4 or sub == -4:
            self.commands.append(Instructions.SPIN180)
            return next_direction
        if sub == -2 or sub == -6:
            self.commands.append(Instructions.SPIN_LEFT)
            return next_direction
        
        raise ArithmeticError('cannot convert path to SPIN command!')
    

    def straight(self, src, dst, direction, has_block):
        """
        交点サークル間の直進コマンドへ変換する。
        """
        # srcからdstの向きとdirectionが同じ向きであることを確認する
        if direction != self.get_next_direction(src, dst):
            # 向きが異なる場合、旋回コマンドに変換する
            pass
        if has_block != False:
            # 始点にブロックがある場合、ブロックありの直進に変換する
            pass
        self.commands.append(Instructions.MOVE_NODE)
        return direction
