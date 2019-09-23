"""
    @file   test_block_bingo_coordinate.py
    @author T.Miyaji
    @brief  block_bingo_coordinateのテストコード
"""
import pytest
from block_bingo_coordinate import Color
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

def create_block_circles(is_left = True, bonus = 6, color = 3):
    return BlockCirclesCoordinate(is_left, bonus, color)


def check_block_circles_size(coordinate):
    # ブロックサークルが8個あることを確認
    assert len(coordinate.block_circles) == 8
    # ブロックサークルの色が1~8番サークルまで格納されていることを確認
    assert len(coordinate.block_circle_color) == 8


def test_init_block_circles_coordinate_left():
    """
    Lコースのブロックサークルの座標と色を格納するデータ構造が正しく生成できることを確認する。
    """
    coordinate = create_block_circles()
    check_block_circles_size(coordinate)


def test_init_block_circles_coordinate_right():
    """
    Rコースのブロックサークルの座標と色を格納するデータ構造が正しく生成できることを確認する。
    """
    coordinate = create_block_circles()
    check_block_circles_size(coordinate)


def test_circle_to_put():
    """
    運搬するブロックの色を指定して、ブロックサークルの座標が正しく返ってくることを確認する。
    """
    coordinate = create_block_circles()
    # 黄色ブロックを運搬するブロックサークルの座標が返ることを確認する
    block_circle = coordinate.circle_to_put(Color.YELLOW)
    assert block_circle in [(0,0), (1,2)]

    # 返却された座標に黄色ブロックを運搬する
    coordinate.move_block(block_circle)
    # 黄色ブロックを運搬するブロックサークルの座標が返ることを確認する
    block_circle = coordinate.circle_to_put(Color.YELLOW)
    assert block_circle in [(0,0), (1,2)]

    # 返却された座標に黄色ブロックを運搬する
    coordinate.move_block(block_circle)
    # Noneが返ってくることを確認する
    assert None == coordinate.circle_to_put(Color.YELLOW)

    # 黒ブロックを運搬するブロックサークルの座標がボーナスサークルの座標であることを確認する
    assert coordinate.get(bonus) == coordinate.circle_to_put(Color.BLACK)
    

def test_get_block_circles_coordinate_error_right():
    """
    誤ったブロックサークル番号を指定したとき、例外が送出されることを確認する。
    """
    with pytest.raises(ValueError):
        coordinate = create_block_circles()
        coordinate.get(9)
        

def test_init_cross_circle_corrdinate():
    """
    交点サークルの座標を格納するデータ構造を作成したとき、はじめは配置ブロックの色がすべてNONEになっていることを確認する。
    """
    coordinate = CrossCirclesCoordinate()
    for y in range(3+1):
        for x in range(3+1):
            assert coordinate.cross_circles[x, y] == Color.NONE


def test_set_block_color():
    """
    交点サークルに置かれたブロックの色を設定すると、データ構造の要素も正しく変わることを確認する。
    """
    coordinate = CrossCirclesCoordinate()
    point = (0,0)
    coordinate.set_block_color(point, Color.RED)
    assert coordinate.color(point) == Color.RED


def test_set_block_color_error():
    """
    誤った座標を指定して交点サークルに置かれたブロックの色を取得した場合、例外が送出されることを確認する。
    """
    with pytest.raises(ValueError):
        coordinate = CrossCirclesCoordinate()
        coordinate.set_block_color((-1,0), Color.BLUE)


def test_goal_node():
    """
    走行体の初期位置とブロックサークルの座標を指定すると、ブロックを設置するための交点サークルの座標が正しく返ることを確認する。
    """
    is_left = True
    bonus = 5
    cross_circles = CrossCirclesCoordinate()
    block_circles = BlockCirclesCoordinate(is_left, bonus)

    assert (1,2) == cross_circles.goal_node((1,1), block_circles.get(3))
    assert (1,2) == cross_circles.goal_node((1,1), block_circles.get(5))
    assert (3,2) == cross_circles.goal_node((2,3), block_circles.get(7))
    assert (1,0) == cross_circles.goal_node((3,0), block_circles.get(1))


def test_move_block_of_cross_circle():
    """
    交点サークルに置かれたブロックを移動させたとき、データ構造の要素がNONEになることを確認する。
    """
    coordinate = CrossCirclesCoordinate()
    point = (0,0)
    coordinate.set_block_color(point, Color.BLUE)
    assert coordinate.color(point) == Color.BLUE

    coordinate.move_block(point)
    assert coordinate.color(point) == Color.NONE