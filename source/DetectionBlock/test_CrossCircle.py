import pytest
from DetectionBlock.BlockBingo import CrossCircle, Color, Block

color = Color.RED


@pytest.fixture
def red_circle():
    return CrossCircle(color, 0)


@pytest.fixture
def blue_block():
    return Block(Color.BLUE)


def test_get_color(red_circle):
    assert red_circle.get_color() == color


def test_set_block(red_circle, blue_block):
    assert red_circle.get_block() is None
    red_circle.set_block(blue_block)
    assert red_circle.get_block() is blue_block


def test_remove_block(red_circle, blue_block):
    red_circle.set_block(blue_block)
    red_circle.remove_block()
    assert red_circle.get_block() is None


def test_default_line(red_circle):
    assert red_circle.lines["up"] is None
    assert red_circle.lines["down"] is None
    assert red_circle.lines["right"] is None
    assert red_circle.lines["left"] is None
