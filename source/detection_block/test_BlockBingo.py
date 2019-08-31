from DetectionBlock.BlockBingo import BlockBingo
import pytest


@pytest.fixture()
def block_bingo():
    return BlockBingo()


def test_size(block_bingo):
    assert len(block_bingo.crossCircles) == 16


def test_line_direction(block_bingo):
    for circle in block_bingo.crossCircles:
        if not(0 <= circle.number <= 4):
            assert circle.lines["up"]["circle"] == block_bingo.crossCircles[circle.number - 4]
        if not (circle.number % 4 == 0):
            assert circle.lines["left"]["circle"] == block_bingo.crossCircles[circle.number - 1]
        if not (circle.number % 4 == 3):
            assert circle.lines["right"]["circle"] == block_bingo.crossCircles[circle.number + 1]
        if not (12 <= circle.number <= 15):
            assert circle.lines["down"]["circle"] == block_bingo.crossCircles[circle.number + 4]


def test_line_num(block_bingo):
    for circle in block_bingo.crossCircles:
        if not(0 <= circle.number <= 4):
            assert circle.lines[circle.number - 4]["circle"] == block_bingo.crossCircles[circle.number - 4]
        if not (circle.number % 4 == 0):
            assert circle.lines[circle.number - 1]["circle"] == block_bingo.crossCircles[circle.number - 1]
        if not (circle.number % 4 == 3):
            assert circle.lines[circle.number + 1]["circle"] == block_bingo.crossCircles[circle.number + 1]
        if not (12 <= circle.number <= 15):
            assert circle.lines[circle.number + 4]["circle"] == block_bingo.crossCircles[circle.number + 4]


def test_get_direction_route(block_bingo):
    assert block_bingo.get_direction_route([0, 1, 2, 6, 10, 11, 15]) \
           == ['right', 'right', 'down', 'down', 'right', 'down']


def test_get_num_route(block_bingo):
    assert block_bingo.get_num_route(['right', 'right', 'down', 'down', 'right', 'down'], 0) \
           == [0, 1, 2, 6, 10, 11, 15]
