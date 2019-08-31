from DetectionBlock.BlockBingo import Line
import pytest


@pytest.fixture()
def line():
    return Line()


def test_get_cost(line):
    assert line.get_cost() == 1


def test_set_cost(line):
    line.set_cost(2)
    assert line.get_cost() == 2
