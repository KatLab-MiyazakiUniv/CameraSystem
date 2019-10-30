"""
    @file   commands.py
    @author T.Miyaji
    @brief  ブロックビンゴ攻略のための運搬経路を走行体動作コマンドに変換する。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

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