# coding: utf-8
"""
@file: block_bingo.py
@author: UEDA Takahiro
@brief: ブロックビンゴエリアのデータ構造
"""

class CrossCircle:
    """
    交点サークル
    """
    def __init__(self, color, block=""):
        self._color = color # 交点サークルの色
        self._block = block # 交点サークルに置いてある置いてあるブロック
        # 交点サークルに繋がっているLine（辺）
        # self.lines[y][x]
        self.lines = {0:{-1:None, 1:None}, 1:{0:None}, -1:{0:None}}

    def get_color(self):
        return self._color

    def set_block(self, block):
        self._block = block

    def get_block(self):
        return self._block


class Line:
    """
    重み付きの辺
    """
    def __init__(self, cost=1):
        self._cost = cost

    def set_cost(self, cost):
        self._cost = cost

    def get_cost(self):
        return self._cost

class BlockBingo:
    """
    左上が基準
    交点サークルとそれに接するLine（辺）を持つ
    """
    def __init__(self):
        # 交点サークルの色の並び
        cross_circles_color = [
            ["R", "R", "B", "B"],
            ["R", "R", "B", "B"],
            ["Y", "Y", "G", "G"],
            ["Y", "Y", "G", "G"]
        ]
        # 交点サークルを生成（コンストラクタで色を設定）
        self.crossCircles = [[CrossCircle(cross_circles_color[y][x]) for x in range(4)] for y in range(4)]

        # 縦のラインを設定
        for y in range(4):
            for x in range(3):
                tmp_line = Line() # 参照渡し
                self.crossCircles[y][x].lines[0][1] = tmp_line
                self.crossCircles[y][x+1].lines[0][-1] = tmp_line
        # 横のラインを設定
        for y in range(3):
            for x in range(4):
                tmp_line = Line() # 参照渡し
                self.crossCircles[y][x].lines[1][0] = tmp_line
                self.crossCircles[y+1][x].lines[-1][0] = tmp_line


def main():
    pass

if __name__ == "__main__":
    main()