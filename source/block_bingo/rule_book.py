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
        candidates = [[1, 2, 3], [3, 5, 8], [6, 7, 8], [1, 4, 6]]

        for candidate in candidates:
            if color_circle in candidate:
                return list(set(candidate) - set([color_circle]))
        raise ValueError('The number of block circle where color block is placed is wrong!')


    def double_bingo(self):
        """
        ダブルビンゴを達成するためにブロックを設置するブロックサークルの番号を返す。
        """
        # カラーブロックが置かれたブロックサークル番号を取得する
        color_circle = self.block_circles.color_circle
        candidates = [[1, 2, 3, 5, 8], [1, 2, 3, 4, 5], 
                      [3, 4, 8, 7, 6], [1, 4, 6, 7, 8]]

        for candidate in candidates:
            if color_circle in candidate:
                return list(set(candidate) - set([color_circle]))
        raise ValueError('The number of block circle where color block is placed is wrong!')

    
    def triple_bingo(self):
        """
        トリプルビンゴを達成するためにブロックを設置するブロックサークルの番号を返す。
        """
        # カラーブロックが置かれたブロックサークル番号を取得する
        color_circle = self.block_circles.color_circle
        candidates = [[1, 2, 3, 5, 8, 7, 6], [1, 2, 3, 4, 6, 7, 8],
                      [3, 5, 8, 7, 6, 4, 1], [6, 4, 1, 2, 3, 5, 8]]
        
        for candidate in candidates:
            if color_circle in candidate:
                return list(set(candidate) - set([color_circle]))
        ValueError('The number of block circle where color block is placed is wrong!')
