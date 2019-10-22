"""
@file: calcPoints.py
@author: Tatsumi0000
@brief: 各頂点の距離を計算する
"""

import numpy as np


def calcPoints(points) -> None:
    """
    ドラッグ・アンド・ドロップした四角形を元に交点サークルの座標を計算
    :param points: 各頂点の座標が
    :type points: numpy.ndarray
    :return None:
    """
    xy_distance = abs(points[0, :] - points[3, :])  # 始点と終点を引いて絶対値を取れば距離になる
    print('各頂点の距離：{}'.format(xy_distance))


# def sortPoints(points: object) -> np.ndarray:
#     """
#     1行目を左上，2行目を右上．3行目を左下．4行目を右下に並び替える関数．
#     :param points: 並べたい座標配列
#     :type points: np.ndarray
#     :return:
#     """
#     points_copy = np.sum(points, axis=1)  # 各行の要素の和
#     max_idx, min_idx = np.argmax(points_copy), np.argmin(points_copy)
#     if min_idx == 0:
#         pass
#     elif min_idx == 1:
#         pass
#
#     print('並べてみた結果：{}'.format(points))
#     return points


if __name__ == '__main__':
    points = np.array([
        [1, 400],
        [1, 300],
        [1, 200],
        [1, 100],
    ])
    print('{}'.format(points))
