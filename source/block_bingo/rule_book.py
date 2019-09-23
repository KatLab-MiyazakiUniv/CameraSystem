"""
    @file   rule_book.py
    @author T.Miyaji
    @brief  ブロックビンゴの終了判定を提供する。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

class RuleBook():
    def __init__(self, block_circles, cross_circles):
        """
        ブロックサークルおよび交点サークルの座標を登録し、ブロックビンゴの終了基準を決定する。

        Parameters
        ----------
        block_circles : BlockCirclesCoordinate
            ブロックサークルの座標
        cross_circles : CrossCirclesCoordinate
            交点サークルの座標
        """
        self.block_circles = block_circles
        self.cross_circles = cross_circles
        
        self.quota = self.single_bingo()
    

    def single_bingo(self):
        """
        シングルビンゴを達成するためにブロックを設置するブロックサークルの番号を返す。
        """
        # カラーブロックが置かれたブロックサークル番号を取得する
        color_circle = self.block_circles.color_circle
        if color_circle in [1, 2, 3]:
            return list(set({1, 2, 3} - set([color_circle])))
        if color_circle in [3, 5, 8]:
            return list(set({3, 5, 8} - set([color_circle])))
        if color_circle in [6, 7, 8]:
            return list(set({6, 7, 8}) - set([color_circle]))
        if color_circle in [1, 4, 6]:
            return list(set({1, 4, 6}) - set([color_circle]))
        raise ValueError('The number of block circle where color block is placed is wrong!')


