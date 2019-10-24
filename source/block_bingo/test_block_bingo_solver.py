"""
    @file   test_block_bingo_solver.py
    @author T.Miyaji
    @brief  block_bingo_solverのテストファイル
"""
import pytest
from block_bingo_solver import Path

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