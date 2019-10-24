"""
@file: calcPoints.py
@author: Tatsumi0000
@brief: 各頂点の距離を計算する
"""

import numpy as np


# def calcPointsDistance(points) -> None:
#     """
#     ドラッグ・アンド・ドロップした四角形を元に交点サークルの座標を計算
#     :param points: 各頂点の座標が
#     :type points: numpy.ndarray
#     :return None:
#     """
#     xy_distance = abs(points[0, :] - points[3, :])  # 始点と終点を引いて絶対値を取れば距離になる
#     print('各頂点の距離：{}'.format(xy_distance))


def calcPoints(points, column) -> np.ndarray:
    """
    現在，3分割，2分割するときは切り捨てにしている
    :param points:
    :param column:
    :return:
    """
    circle_points = np.zeros((column, 2), dtype=int)
    x_distance = points[1, 0] - points[0, 0]  # xの距離
    y_distance = points[2, 1] - points[0, 1]  # yの距離
    # print('前{0}'.format(circle_points))
    if column == 8:  # ブロックサークルのとき
        # x座標
        circle_points[0, 0] = circle_points[3, 0] = circle_points[5, 0] = points[0, 0]
        circle_points[1, 0] = circle_points[6, 0] = x_distance * 1 // 2 + points[0, 0]
        circle_points[2, 0] = circle_points[4, 0] = circle_points[7, 0] = points[1, 0]
        # y座標
        circle_points[0:4, 1] = points[0, 1]
        circle_points[3:5, 1] = y_distance * 1 // 2 + points[0, 1]
        circle_points[5:, 1] = points[3, 1]
    elif column == 16:  # 交点サークルのとき
        # x座標
        circle_points[0:13:4, 0] = points[0, 0]
        circle_points[1:14:4, 0] = x_distance * 1 // 3 + points[0, 0]
        circle_points[2:15:4, 0] = x_distance * 2 // 3 + points[0, 0]
        circle_points[3:16:4, 0] = points[3, 0]
        # y座標
        circle_points[0:4, 1] = points[0, 1]
        circle_points[4:8, 1] = y_distance * 1 // 3 + points[0, 1]
        circle_points[8:12, 1] = y_distance * 2 // 3 + points[0, 1]
        circle_points[12:, 1] = points[3, 1]
    else:
        return "値が不正です．"

    print("座標計算結果：{}".format(circle_points))
    return circle_points


if __name__ == '__main__':
    points = np.array([
        [100, 400],
        [100, 800],
        [800, 400],
        [800, 800],
    ])
    cc_points = np.zeros((16, 2))
    # print('足す前{}'.format(points))
    print('足した後{}'.format(calcPoints(points, cc_points)))
