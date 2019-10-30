"""
    @file   test_block_bingo_solver.py
    @author T.Miyaji
    @brief  block_bingo_solverのテストファイル
"""
import pytest
from block_bingo_solver import Path
from block_bingo_solver import BlockBingoSolver
from block_bingo_solver import BlockCirclesCoordinate
from block_bingo_solver import CrossCirclesCoordinate
from block_bingo_coordinate import Color
from commands import Instructions

def create_block_bingo(path=[(1,0), (2,0), (2,1)], is_left=True, bonus=5, color=3):
    return BlockBingoSolver(BlockCirclesCoordinate(is_left, bonus, color), CrossCirclesCoordinate(), path)


def test_path():
    """
    Pathクラスのテスト。
    """
    path = Path()
    # (0,1) => (0,2)の経路を登録
    path.set_path((0,1), (0,2))
    # (0,1) => (0,2)の経路が登録されていることを確認
    assert (0,1) == path.get((0,2))
    
    # (0,1) => (0,3)の経路を登録
    path.set_path((0,1), (0,3))
    # (0,1) => (0,3)の経路が登録されていることを確認
    assert (0,1) == path.get((0,3))

    # 経路[(0,1), (0,2)]が取得できることを確認
    assert [(0,1), (0,2)] == path.search_path((0,1), (0,2))
    # 経路[(0,1). (0,3)]が取得できることを確認
    assert [(0,1), (0,3)] == path.search_path((0,1), (0,3))


def test_path_invalid():
    """
    Pathクラスのテスト。不正な入力ver.
    """
    with pytest.raises(ArithmeticError):
        path = Path()
        # (0,1) => (0,2)の経路を登録
        path.set_path((0,1), (0,2))
        # (0,2) => (0,3)の経路を登録
        path.set_path((0,2), (0,3))
        # 存在しない始点を入力として運搬経路を取得する
        path.search_path((1,2), (0,3))


def test_get_robot_position_north():
    solver = create_block_bingo([(1,0), (0,0)])
    assert (1,0.5) == solver.position
    assert 0 == solver.direction


def test_get_robot_direction_east():
    solver = create_block_bingo([(0,0), (0,1), (0,2)])
    assert (0.5,2) == solver.position
    assert 2 == solver.direction


def test_get_robot_direction_south():
    solver = create_block_bingo([(0,2), (1,2), (2,2)])
    assert (2,2.5) == solver.position
    assert 4 == solver.direction


def test_get_robot_direction_west():
    solver = create_block_bingo([(2,2), (2,1), (2,0)])
    assert (2.5,1) == solver.position
    assert 6 == solver.direction


def test_Manhattan_distance():
    solver = create_block_bingo([(2,2), (2,1), (2,0)])
    assert 4 == solver.Manhattan_distance((3,1), (0,2))
    assert 2 == solver.Manhattan_distance((3,1), (2,0))
    assert 2 == solver.Manhattan_distance((3,1), (1,1))
    assert 5 == solver.Manhattan_distance((3,1), (0,3))
    assert 3.5 == solver.Manhattan_distance((3,1), (1, 2.5))


def test_current_direction():
    solver = create_block_bingo([(1,0), (2,0), (2,1)])
    # 走行体の現在地と向きを確認する
    assert (2.5,1) == solver.position
    assert 2 == solver.direction

    # (2.5,1) => (2,1) => (2,2)に移動する
    path = Path()
    path.set_path((2.5,1), (2,1))
    solver.direction = 0
    solver.position = (2,1)
    # 走行体の向きが北向きになっていることを確認する
    assert 0 == solver.current_direction((2,1), path)
    path.set_path((2,1), (2,2))
    # 走行体の向きが東向きになっていることを確認する
    assert 2 == solver.current_direction((2,2), path)


def test_adjacent_nodes():
    solver = create_block_bingo([(1,0), (2,0), (2,1)])
    # 走行体の現在地(3,1)の隣接ノードが正しく計算できていることを確認する
    assert [(2.5,1), (3,0.5), (3,1.5)] == solver.adjacent_nodes((3,1))
    # ノード(1,1)の隣接ノードが正しく計算できていることを確認する
    assert [(0.5,1), (1.5,1), (1, 0.5), (1, 1.5)] == solver.adjacent_nodes((1,1))
    # ノード(3,3)の隣接ノードが正しく計算できていることを確認する
    assert [(2.5,3), (3,2.5)] == solver.adjacent_nodes((3,3))


def test_moving_cost():
    solver = create_block_bingo([(0,0), (0,1)])
    # 走行体の現在地と向きを確認する
    assert (0.5,1) == solver.position
    assert 2 == solver.direction
    path = Path()

    # (1,1)まで移動する
    solver.position = (1,1)
    solver.direction = 4
    solver.cross_circles.move_block((1,1))

    #　--ブロックなしの動作--
    # 走行体が水平に進むとき
    solver.direction = 2 # 東向きに設定
    assert 1 == solver.moving_cost((1,1), (1,1.5), path)    # 直進
    assert 2 == solver.moving_cost((1,1), (1,0.5), path)    # 180度旋回
    solver.direction = 4 # 南向きに設定
    assert 2 == solver.moving_cost((1,1), (1,0.5), path)    # 右に90度旋回
    assert 2 == solver.moving_cost((1,1), (1,1.5), path)    # 左に90度旋回

    # 走行体が垂直に進むとき
    solver.direction = 4 # 南向きに設定
    assert 1 == solver.moving_cost((1,1), (1.5,1), path)    # 直進
    assert 2 == solver.moving_cost((1,1), (0.5,1), path)    # 180度旋回
    solver.direction = 2 # 東向きに設定
    assert 2 == solver.moving_cost((1,1), (1.5,1), path)    # 右に90度旋回
    assert 2 == solver.moving_cost((1,1), (0.5,1), path)    # 左に90度旋回
    
    # --ブロックありの動作--
    # 走行体が水平に進むとき
    solver.direction = 2 # 東向きに設定
    solver.cross_circles.open.append((1,1)) # ブロックを設置
    assert 4 == solver.moving_cost((1,1), (1,1.5), path)    # 直進
    assert 5 == solver.moving_cost((1,1), (1,0.5), path)    # 180度旋回
    solver.direction = 4 # 南向きに設定
    assert 2 == solver.moving_cost((1,1), (1,0.5), path)    # 右に90度旋回
    assert 2 == solver.moving_cost((1,1), (1,1.5), path)    # 左に90度旋回

    # 走行体が垂直に進むとき
    solver.direction = 4 # 南向きに設定
    assert 4 == solver.moving_cost((1,1), (1.5,1), path)    # 直進
    assert 5 == solver.moving_cost((1,1), (0.5,1), path)    # 180度旋回
    solver.direction = 2 # 東向きに設定
    assert 2 == solver.moving_cost((1,1), (1.5,1), path)    # 右に90度旋回
    assert 2 == solver.moving_cost((1,1), (0.5,1), path)    # 左に90度旋回


def test_a_star():
    # 走行体の現在地は(1,1)、向きは東向き
    solver = create_block_bingo([(1,0), (0,0)])
    solver.direction = 2
    solver.position = (1,1)
    solver.cross_circles.move_block((1,1))
    # (1,1)から(0,2)まで運搬する経路を計算する
    assert [(1,1), (1,1.5), (1,2), (0.5,2), (0,2)] == solver.a_star((1,1), (0,2))


def test_a_star2():
    # 走行体の現在地は(3,1)、向きは西向き
    solver = create_block_bingo([(2,1), (2,0)])
    solver.direction = 6
    solver.position = (3,1)
    solver.cross_circles.move_block((3,1))
    # (3,1)から(1,0)まで運搬する経路を計算する
    assert [(3,1), (2.5,1), (2,1), (1.5,1), (1,1), (1,0.5), (1,0)] == solver.a_star((3,1), (1,0))


def test_a_star3():
    """
    分析モデル2.3.5節の計算例をもとに動作を確認する。
    """
    # 走行体の現在地は(2,0)、向きは北向き
    solver = create_block_bingo([(2,0), (1,0)])
    solver.direction = 0
    solver.position = (2,0)
    solver.cross_circles.move_block((2,0))
    # 走行体の向きを東向きにする
    solver.direction = 2
    # (2,2)のブロックを運搬したことにする
    solver.cross_circles.move_block((2,2))
    # (2,0)から(1,2)まで運搬する経路を計算する
    assert [(2,0), (2,0.5), (2,1), (2,1.5), (2,2), (1.5,2), (1,2)] == solver.a_star((2,0), (1,2))


def test_solve2():
    solver = create_block_bingo([(1,0), (2,0)], bonus=6, color=7)
    block = [[Color.YELLOW, Color.NONE, Color.YELLOW, Color.NONE],
             [Color.NONE, Color.GREEN, Color.NONE, Color.BLUE],
             [Color.RED, Color.NONE, Color.BLACK, Color.NONE],
             [Color.NONE, Color.BLUE, Color.NONE, Color.GREEN]]
    for x in range(0, 3+1):
        for y in range(0, 3+1):
            solver.cross_circles.set_block_color((x,y), block[x][y])

    commands = ['e', 'm', 'u', 'f', 'u', 'u', 'y', 'u', 'u', 'e', 'u', 'u', 'z', 'e', 'u', 'u', 'e', 'u', 'u', 'z']
    assert commands == solver.solve()