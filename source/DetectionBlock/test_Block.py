from DetectionBlock.BlockBingo import Block, Color
import pytest


@pytest.fixture()
def none_block():
    return Block()


@pytest.fixture()
def red_block():
    return Block(Color.RED)


def test_default_block(none_block):
    assert none_block._color is None


def test_get_block(red_block):
    assert red_block.get_color() is Color.RED


def test_set_block(red_block):
    red_block.set_color(Color.BLUE)
    assert red_block.get_color() is Color.BLUE
