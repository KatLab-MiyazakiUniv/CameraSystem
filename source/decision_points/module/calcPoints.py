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
    :type points: ndarray
    :return None:
    """
    xy_distance = abs(points[0, :] - points[3, :])  # 始点と終点を引いて絶対値を取れば距離になる
    print('各頂点の距離：{}'.format(xy_distance))