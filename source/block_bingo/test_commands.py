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
    commands = create_commands()
    
    src = (3,1)
    dst = (2.5,1)
    direction = 4   # 南に向いていると仮定
    has_block = False

    # 走行体が回頭したのち、北向きになることを確認する
    assert 0 == commands.spin(src, dst, direction, has_block)
    assert 1 == len(commands.get())
    assert Instructions.SPIN180 == commands.get()[0]


def test_straight():
    commands = create_commands()

    src = (1,1)
    dst = (1,1.5)
    direction = 2
    has_block = False

    assert direction == commands.straight(src, dst, direction, has_block)
    assert 1 == len(commands.get())
    assert Instructions.MOVE_NODE == commands.get()[0]


def test_turn():
    commands = create_commands()

    src = (1,1)
    dst = (1,1.5)
    direction = 0
    has_block = False

    assert 2 == commands.turn(src, dst, direction, has_block)
    assert 1 == len(commands.get())
    assert Instructions.TURN_RIGHT90_UNEXIST_BLOCK == commands.get()[0]


def test_turn180():
    commands = create_commands()

    src = (1,1)
    dst = (1.5,1)
    direction = 0
    has_block = False

    assert 4 == commands.turn180(src, dst, direction, has_block)
    assert 1 == len(commands.get())
    assert Instructions.TURN180 == commands.get()[0]