"""
@file: test_get_circle_point.py
@author: Tatsumi0000
@brief: GetCirclePoint.pyのをテストするプログラム
"""

from GetCirclePoint import GetCirclePoint
import numpy as np


def test_calcPoints():
    get_circle_point = GetCirclePoint()
    points = np.array([[0, 0], [100, 0], [0, 400], [100, 400]])
    cc_points = get_circle_point.calc_points(points, 16)
    assert cc_points[1, 0] == 33
    assert cc_points[8, 1] == 266
    assert cc_points[10, 0] == 66
    assert cc_points[10, 1] == 266


def test_add():
    get_circle_point = GetCirclePoint()
    cc_points = np.array([[110, 10], [410, 10], [10, 413], [410, 413]])
    bc_points = np.array([[160, 20], [460, 20], [160, 460], [460, 460]])
    get_circle_point.cc_points = get_circle_point.calc_points(cc_points, 16)
    get_circle_point.bc_points = get_circle_point.calc_points(bc_points, 8)
    get_circle_point.add()
    assert get_circle_point.named_points['b1'][0] == 160
    assert get_circle_point.named_points['b1'][1] == 20
    assert get_circle_point.named_points['c00'][0] == 110
    assert get_circle_point.named_points['c11'][0] == 210
    assert get_circle_point.named_points['c11'][1] == 144
