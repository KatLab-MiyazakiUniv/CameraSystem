"""
    @file   test_block_bingo_coordinate.py
    @author T.Miyaji
    @brief  block_bingo_coordinateのテストコード
"""
import pytest
from block_bingo_coordinate import Color
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate

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


def test_move_block():
    """
    引数の座標をキーにもつブロックサークル番号がopenリストから削除されることを確認する。
    """
    is_left = True
    bonus = 4
    coordinate = BlockCirclesCoordinate(is_left, bonus)
    
    # openリストに1番サークルが登録されていることを確認する
    assert 1 in coordinate.open
    # 1番サークルにブロックを設置する
    coordinate.move_block(coordinate.get(1))
    # openリストから1番サークルが削除されていることを確認する
    assert 1 not in coordinate.open


def test_move_block_invalid():
    """
    存在しないブロックサークルの座標を引数にしてmove_block関数を呼び出す。
    """
    is_left = True
    bonus = 4
    coordinate = BlockCirclesCoordinate(is_left, bonus)

    # openリストを取得しておく
    open = coordinate.open
    # 存在しないブロックサークルの座標を引数にしてmove_blockを呼び出す
    coordinate.move_block((5,5))
    # openリストに影響がないことを確認する
    assert open == coordinate.open



def test_circle_to_put():
    """
    運搬するブロックの色を指定して、ブロックサークルの座標が正しく返ってくることを確認する。
    """
    is_left = True
    bonus = 5
    coordinate = BlockCirclesCoordinate(is_left, bonus)
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
        is_left = True
        bonus = 5
        coordinate = BlockCirclesCoordinate(is_left, bonus)
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