# coding: utf-8
"""
@file: block_bingo.py
@author: UEDA Takahiro
@brief: ブロックビンゴエリアのデータ構造
"""
from enum import Enum
from typing import List


class Color(Enum):
    """
    ブロックやラインの色
    """
    RED = 0
    BLUE = 1
    YELLO = 2
    GREEN = 3
    BLACK = 4
    WHITE = 5


class Block:
    def __init__(self, color=None):
        """
        カラークラスを渡す
        """
        self._color = color

    def get_color(self):
        """
        カラークラスをのメンバ変数を返す
        ブロックがない場合は"None"を返す
        """
        return self._color

    def set_color(self, color):
        """
        カラークラスのメンバ変数を渡す
        """
        self._color = color


class CrossCircle:
    """
    交点サークル
    """

    def __init__(self, color, number):
        self._color = color  # 交点サークルの色
        self._block = Block()  # 交点サークルに置いてあるブロック
        self.number = number
        # 交点サークルに繋がっているLine（辺）
        # self.lines[y][x]
        self.lines = {"left": None, "right": None, "up": None, "down": None}

    def get_color(self):
        """
        交点サークルの色を取得する
        """
        return self._color

    def set_block(self, block):
        """
        ブロックを置く（色）
        """
        self._block.set_color(block)

    def get_block(self):
        """
        ブロック（色）を取得する
        ブロックが存在しない場合は、None
        """
        return self._block.get_color()

    def remove_block(self):
        """
        ブロックを取り除く（色をNoneに設定）
        """
        self._block.set_color(None)


class BlockBingo:
    """
    左上が基準
    交点サークルとそれに接するLine（辺）を持つ
    """

    def __init__(self):
        self.crossCircles = None
        self._create_network()

    def _create_network(self):
        def _update(num_key, direction_key):
            circle.lines[num_key] = circle.lines[direction_key] = {"circle": self.crossCircles[num_key],
                                                                   "direction": direction_key,
                                                                   "num": num_key
                                                                   }
        # 交点サークルの色の並び
        cross_circles_color = [
            Color.RED, Color.RED, Color.BLUE, Color.BLUE,
            Color.RED, Color.RED, Color.BLUE, Color.BLUE,
            Color.YELLO, Color.YELLO, Color.GREEN, Color.GREEN,
            Color.YELLO, Color.YELLO, Color.GREEN, Color.GREEN
        ]
        # 交点サークルを生成（コンストラクタで色を設定）
        self.crossCircles = [CrossCircle(cross_circles_color[i], i) for i in range(16)]

        for circle in self.crossCircles:
            num = circle.number
            if num % 4 != 0:  # いちばん左の列以外
                _update(num - 1, "left")
            if num % 4 != 3:  # いちばん右の列以外
                _update(num + 1, "right")
            if not (0 <= num <= 3):  # いちばん上の列以外
                _update(num - 4, "up")
            if not (12 <= num <= 15):  # いちばん下の列以外
                _update(num + 4, "down")

    def get_direction_route(self, route_list: List[int]) -> List[str]:
        """
        数字のルートを方角のルートに変換して取得する。
        :param route_list: 数字のルート
        :return: 方角のルート
        """
        directions = []
        _route_list = list(route_list)
        now_place = _route_list.pop(0)
        for place in _route_list:
            directions.append(self.crossCircles[now_place].lines[place]["direction"])
            now_place = place
        return directions

    def get_num_route(self, route_list: List[str], now_place: int) -> List[int]:
        """
        方角のルートを数字のルートに変換して取得する。
        :param route_list: 方角のルート
        :param now_place: 現在地
        :return: 数字のルート
        """
        nums = [now_place]
        for direction in route_list:
            num = self.crossCircles[now_place].lines[direction]["num"]
            nums.append(num)
            now_place = num
        return nums


def main():
    """
    # 交点サークルの座標(インデックス?)に関して
        (0, 0)            (3, 0)
        ↓                 ↓
        O-----O-----O-----O
        |  1  |  2  |  3  |
        O-----O-----O-----O
        |  4  |     |  5  |
        O-----O-----O-----O
        |  6  |  7  |  8  |
        O-----O-----O-----O
        ↑                 ↑
        (0, 3)            (3, 3)

    # ブロック配置の表現方法
        K-----O-----G-----O
        |  O  |  O  |  O  |
        O-----Y-----O-----B
        |  O  |  O  |  K  |
        Y-----O-----G-----O
        |  O  |  R  |  O  |
        O-----R-----O-----B
    ## 各文字とブロックの色対応
    - R: Color.RED
    - G: Color.GREEN
    - B: Color.BLUE
    - K: Color.BLACK
    - O: None（ブロック無し）
    """
    # NOTE: ブロックサークル部分未実装
    blk_bingo = BlockBingo()

    x, y = 0, 0
    blk_bingo.crossCircles[y][x].set_block(Color.BLACK)
    x, y = 0, 2
    blk_bingo.crossCircles[y][x].set_block(Color.YELLO)
    x, y = 1, 1
    blk_bingo.crossCircles[y][x].set_block(Color.YELLO)
    x, y = 1, 3
    blk_bingo.crossCircles[y][x].set_block(Color.RED)
    x, y = 2, 0
    blk_bingo.crossCircles[y][x].set_block(Color.GREEN)
    x, y = 2, 2
    blk_bingo.crossCircles[y][x].set_block(Color.GREEN)
    x, y = 3, 1
    blk_bingo.crossCircles[y][x].set_block(Color.BLUE)
    x, y = 3, 3
    blk_bingo.crossCircles[y][x].set_block(Color.BLUE)

    """
    # 交点サークルに接するラインに関して
              ↓この交点サークルを例に考える
        O-----O-----O-----O
        |  1  |  2  |  3  |
        O-----O-----O-----O
        |  4  |     |  5  |
        O-----O-----O-----O
        |  6  |  7  |  8  |
        O-----O-----O-----O
    """
    cc_x, cc_y = 1, 0  # 交点サークルの座標
    dir_x, dir_y = 0, -1  # 向かって上のライン（存在しない）
    blk_bingo.crossCircles[cc_y][cc_x].lines[dir_y][dir_x]  # None
    dir_x, dir_y = 0, 1  # 向かって下のライン
    blk_bingo.crossCircles[cc_y][cc_x].lines[dir_y][dir_x].get_cost()  # 1（デフォルトでコストは1に設定されている）
    dir_x, dir_y = -1, 0  # 向かって左のライン
    blk_bingo.crossCircles[cc_y][cc_x].lines[dir_y][dir_x].set_cost(100)  # コストを100に設定
    dir_x, dir_y = 1, 0  # 向かって右のライン
    blk_bingo.crossCircles[cc_y][cc_x].lines[dir_y][dir_x].set_cost(100)  # コストを100に設定
    blk_bingo.crossCircles[cc_y][cc_x].lines[dir_y][dir_x].get_cost()  # 100


if __name__ == "__main__":
    main()
