from DetectionBlock.BlockBingo import BlockBingo
import pytest


@pytest.fixture()
def block_bingo():
    return BlockBingo()


def test_size(block_bingo):
    assert len(block_bingo.crossCircles) == 16


"""
def test_line_direction(block_bingo):
    for circle_line in block_bingo.crossCircles:
        for circle in circle_line:
            print(circle.lines[0][-1])
"""