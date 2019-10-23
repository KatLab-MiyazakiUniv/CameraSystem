"""
    @file   test_block_bingo_coordinate.py
    @author T.Miyaji
    @brief  block_bingo_coordinateのテストコード
"""
import pytest
from block_bingo_coordinate import Color
from block_bingo_coordinate import BlockCirclesCoordinate

def check_block_circles_size(coordinate):
    # ブロックサークルが8個あることを確認
    assert len(coordinate.block_circles) == 8
    # ブロックサークルの色が1~8番サークルまで格納されていることを確認
    assert len(coordinate.block_circle_color) == 8


def test_init_block_circles_coordinate_left():
    """
    Lコースのブロックサークルの座標と色を格納するデータ構造が正しく生成できることを確認する。
    """
    is_left = True
    bonus = 6
    coordinate = BlockCirclesCoordinate(is_left, bonus)
    check_block_circles_size(coordinate)


def test_init_block_circles_coordinate_right():
    """
    Rコースのブロックサークルの座標と色を格納するデータ構造が正しく生成できることを確認する。
    """
    is_left = False
    bonus = 4
    coordinate = BlockCirclesCoordinate(is_left, bonus)
    check_block_circles_size(coordinate)