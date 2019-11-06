"""
@file: test_MoveGetCirclePoint.py
@author: Tatsumi0000
@brief: 取得した座標をtkinterで描画し，マウスで動かせるようにし座標の微調整をする．
"""

import pytest
import tkinter as tk
from GetCirclePoint import GetCirclePoint
from MoveGetCirclePoint import MoveGetCirclePoint, Points


@pytest.fixture()
def move_get_circle_point():
    root = tk.Tk()
    move_get_circle_point = MoveGetCirclePoint(master=root)
    return move_get_circle_point


def test_set_get_circle_point(move_get_circle_point):
    get_circle_point = GetCirclePoint()
    move_get_circle_point.set_get_circle_point(get_circle_point)
    assert move_get_circle_point.get_circle_point == get_circle_point


def test_points():
    points = Points()
    assert points.ix == 0
    assert points.iy == 0
    assert points.item_id == ()
    points.ix = 100
    points.iy = 200
    assert points.ix == 100
    assert points.iy == 200
    points.item_id = (1, 2)
    assert points.item_id == (1, 2)
