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

def create_block_bingo(path=[(1,0), (2,0), (2,1)]):
    is_left = True
    bonus = 5
    return BlockBingoSolver(BlockCirclesCoordinate(is_left, bonus), CrossCirclesCoordinate(), path)


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
    assert (1,1) == solver.position
    assert 2 == solver.direction


def test_get_robot_direction_east():
    solver = create_block_bingo([(0,0), (0,1), (0,2)])
    assert (0,2) == solver.position
    assert 0 == solver.direction


def test_get_robot_direction_west():
    solver = create_block_bingo([(0,2), (1,2), (2,2)])
    assert (2,2) == solver.position
    assert 6 == solver.direction


def test_get_robot_direction_south():
    solver = create_block_bingo([(2,2), (2,1), (2,0)])
    assert (3,1) == solver.position
    assert 4 == solver.direction


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
    assert (3,1) == solver.position
    assert 4 == solver.direction

    # (3,1) => (3,2) => (2,2)に移動する
    path = Path()
    path.set_path((3,1), (3,2))
    # 走行体の向きが東向きになっていることを確認する
    assert 2 == solver.current_direction((3,2), path)
    path.set_path((3,2), (2,2))
    # 走行体の向きが北向きになっていることを確認する
    assert 0 == solver.current_direction((2,2), path)


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
    assert (1,1) == solver.position
    assert 4 == solver.direction
    path = Path()

    #　--ブロックなしの動作--
    # 走行体が水平に進むとき
    solver.direction = 2 # 東向きに設定
    assert 1 == solver.moving_cost((1,1), (1,1.5), path)    # 直進
    assert 1 == solver.moving_cost((1,1), (1,0.5), path)    # 180度旋回
    solver.direction = 4 # 南向きに設定
    assert 2 == solver.moving_cost((1,1), (1,0.5), path)    # 右に90度旋回
    assert 2 == solver.moving_cost((1,1), (1,1.5), path)    # 左に90度旋回

    # 走行体が垂直に進むとき
    solver.direction = 4 # 南向きに設定
    assert 1 == solver.moving_cost((1,1), (1.5,1), path)    # 直進
    assert 1 == solver.moving_cost((1,1), (0.5,1), path)    # 180度旋回
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