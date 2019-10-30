"""
    @file   rule_book.py
    @author T.Miyaji
    @brief  ブロックビンゴの終了判定を提供する。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate
from enum import Enum, auto

class Bingo(Enum):
    SINGLE_BINGO = auto()
    DOUBLE_BINGO = auto()
    TRIPLE_BINGO = auto()
    FULL_BINGO = auto()


class RuleBook():
    def __init__(self, block_circles, cross_circles, bingo):
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
        
        # ボーナスサークル設置成功数
        self.bonus = 1
        # ビンゴ達成のためのノルマ
        self.quota = self.select_bingo_quota(bingo)
    

    def select_bingo_quota(self, bingo):
        """
        ブロックビンゴ達成のためのノルマを決める。
        
        Parameters
        ----------
        bingo : Bingo
            ビンゴの種類
        """
        if bingo == Bingo.SINGLE_BINGO:
            return self.single_bingo()
        if bingo == Bingo.DOUBLE_BINGO:
            return self.double_bingo()
        if bingo == Bingo.TRIPLE_BINGO:
            return self.triple_bingo()
        if bingo == Bingo.FULL_BINGO:
            return self.full_bingo()
        
        raise ValueError('selected quota is not in Bingo enumeration!')


    def single_bingo(self):
        """
        シングルビンゴを達成するためにブロックを設置するブロックサークルの番号を返す。
        """
        # カラーブロックが置かれたブロックサークル番号を取得する
        color_circle = self.block_circles.color_circle
        candidates = [[1, 2, 3], [3, 5, 8], [6, 7, 8], [1, 4, 6]]

        for candidate in candidates:
            if color_circle in candidate:
                candidate.remove(color_circle)
                return candidate
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
                candidate.remove(color_circle)
                return candidate
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
                candidate.remove(color_circle)
                return candidate
        raise ValueError('The number of block circle where color block is placed is wrong!')


    def full_bingo(self):
        """
        フルビンゴを達成するためにブロックを設置するブロックサークルの番号を返す。
        """
        # カラーブロックが置かれたブロックサークル番号を取得する
        color_circle = self.block_circles.color_circle
        candidate = [number for number in range(1, 8+1)]

        if color_circle in candidate:
            candidate.remove(color_circle)
            return candidate
        raise ValueError('The number of block circle where color block is placed is wrong!')

    
    def get_quota(self):
        """
        ブロックビンゴ攻略までに設置する必要があるブロックサークル番号を返す。
        """
        return self.quota


    def achivement(self):
        """
        ゲームの終了判定をする。
        """
        if len(self.quota) == 0 and self.bonus == 2:
            return True
        return False
    

    def put_color_block(self, index):
        """
        有効移動が成立したことを登録する。

        Parameters
        ----------
        index : tuple
            quotaのインデックス
        """
        if 0 <= index < len(self.quota):
            del self.quota[index]
    

    def put_black_block(self):
        """
        ボーナスサークル設置が成立したことを登録する。
        """
        self.bonus += 1