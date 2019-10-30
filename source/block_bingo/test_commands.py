"""
    @file   test_commands.py
    @author T.Miyaji
    @brief  commandsのテストコード
"""
from commands import Instructions
from commands import Commands
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate
import pytest

def test_translate():
    order = [Instructions.ENTER_BINGO_AREA_L6,
             Instructions.STRAIGHT,
             Instructions.STRAIGHT,
             Instructions.SPIN_LEFT,
             Instructions.PUT]
    instructions = Instructions()
    order = [instructions.translate(e) for e in order]

    assert order[0] == '6番サークルに進入'
    assert order[1] == 'ブロックサークル間を直進'
    assert order[2] == 'ブロックサークル間を直進'
    assert order[3] == '左に90°回頭する'
    assert order[4] == 'ブロックを黒線の中点から設置'


def create_commands(is_left=True, bonus=5, color=3):
    block_circles = BlockCirclesCoordinate(is_left, bonus, color)
    cross_circles = CrossCirclesCoordinate()

    return Commands(block_circles, cross_circles)

def test_spin():
    # README.mdの1.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (1,1.5), 0, False],
            [(1,1), (1,1.5), 4, False],
            [(1,1), (1,0.5), 0, False],
            [(1,1), (1,0.5), 4, False]]
    
    # 期待出力: 次の走行体の向き, コマンド
    results = [[2, 'd'],
              [2, 'e'],
              [6, 'e'],
              [6, 'd']]

    for arg, result in zip(args, results):
        commands = create_commands()
        assert result[0] == commands.spin(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert result[1] == commands.get()[0] 


def test_straight():
    # README.mdの2.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (0.5,1), 0, False],
            [(1,1), (1,1.5), 2, False],
            [(1,1), (1.5,1), 4, False],
            [(1,1), (1,0.5), 6, False]]

    for arg in args:
        commands = create_commands()
        assert arg[2] == commands.straight(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert 'u'== commands.get()[0]


def test_turn():
    # README.mdの3.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (1,1.5), 0, False],
            [(1,1), (1,0.5), 0, False]]

    # 期待出力リスト: 次の走行体の向き, コマンド
    results = [[2, 'k'], [6, 'm']]

    for (arg, result) in zip(args, results):
        commands = create_commands()
        assert result[0] == commands.turn(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert result[1] == commands.get()[0]


def test_turn180():
    # README.mdの4.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (1.5,1), 0, False],
            [(1,1), (1,0.5), 2, False],
            [(1,1), (0.5,1), 4, False],
            [(1,1), (1,1.5), 6, False]]

    # 期待出力リスト: 次の走行体の向き, コマンド
    results = [[4, 'n'], [6, 'n'], [0, 'n'], [2, 'n']]

    for (arg, result) in zip(args, results):
        commands = create_commands()
        assert result[0] == commands.turn180(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert result[1] == commands.get()[0]


def test_straight_detour():
    # README.mdの5.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,0), (0.5,0), 0, True],
            [(3,1), (3,0.5), 6, True],
            [(2,3), (1.5,3), 0, True],
            [(3,2), (3,2.5), 2, True]]
    
    # 期待出力リスト: コマンド
    results = ['h', 'h', 'i', 'i']

    for (arg, result) in zip(args, results):
        commands = create_commands()
        commands.commands.append('u')   # 直進コマンドを追加する
        assert arg[2] == commands.straight_detour(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert result[0] == commands.get()[0]


def test_turn_detour():
    # README.mdの6.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (1,1.5), 0, True],
            [(1,1), (1,0.5), 0, True]]
    
    # 期待出力リスト: 次の走行体の向き, コマンド
    results = [[2, 'j'], [6, 'l']]

    for (arg, result) in zip(args, results):
        commands = create_commands()
        commands.commands.append('u')    # 直進コマンドを追加する
        assert result[0] == commands.turn_detour(arg[0], arg[1], arg[2], arg[3])
        assert 1 == len(commands.get())
        assert result[1] == commands.get()[0]


def test_turn180_detour():
    # README.mdの7.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1,1), (1,1.5), 6, True],
            [(0,2), (0,1.5), 2, True]]
    
    # 期待出力リスト: 次の走行体の向き, コマンド
    results = [[2, 'f', 'h'], [6, 'f', 'i']]

    for (arg, result) in zip(args, results):
        commands = create_commands()
        commands.commands.append('u')   # 直進コマンドを追加する
        assert result[0] == commands.turn180_detour(arg[0], arg[1], arg[2], arg[3])
        assert 2 == len(commands.get())
        assert result[1] == commands.get()[0]
        assert result[2] == commands.get()[1]


def test_put_block_from_midpoint():
    # README.mdの8.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    args = [[(1.5,1), (1,0), 0, False],
            [(2,0.5), (1,0), 2, False],
            [(1.5,0), (1,0), 0, False],
            [(1,0.5), (1,0), 2, False]]
    # 期待出力リスト: 次の走行体の向き, コマンド
    results = [[6, 'e', 'g'], [0, 'e', 'g'], [2, 'd', 'g'], [4, 'd', 'g']]

    for (arg, result) in zip(args, results):
        commands = create_commands()
        assert result[0] == commands.put_block_from_midpoint(arg[0], arg[1], arg[2], arg[3])
        assert 2 == len(commands.get())
        assert result[1] == commands.get()[0]
        assert result[2] == commands.get()[1]


def test_put_block_from_cross_circle():
    # README.mdの9.1のコマンド変換例
    # 引数リスト: 始点, 終点, 現在の走行体の向き, 始点にブロックがあるか
    points = [(1,0), (1,1), (2,0), (2,1)]   # 交点サークルの座標
    place = (1,0)   # 設置するブロックサークルの座標

    args_list = []
    for point in points:
        args_list.append([[point, place, i*2, False] for i in range(0,4)])
    
    # 期待出力リスト: 次の走行体の向き, コマンド
    results_list = [[[2, 'd', 'y'], [2, 'y'], [4, 'z'], [4, 'e', 'z']],
               [[6, 'e', 'z'], [4, 'd', 'y'], [4, 'y'], [6, 'z']],
               [[0, 'y'], [2, 'z'], [2, 'e', 'z'], [0, 'd', 'y']],
               [[0, 'z'], [0, 'e', 'z'], [6, 'd', 'y'], [6, 'y']]]
    
    for (args, results) in zip(args_list, results_list):
        for (arg, result) in zip(args, results):
            commands = create_commands()
            print(arg[0], arg[1], arg[2], arg[3], result[0], result[1])
            assert result[0] == commands.put_block_from_cross_circle(arg[0], arg[1], arg[2], arg[3])
            print(commands.get())
            assert len(result)-1 == len(commands.get())
            if len(commands.get()) == 1:
                assert result[1] == commands.get()[0]
            else:
                assert result[1] == commands.get()[0]
                assert result[2] == commands.get()[1]