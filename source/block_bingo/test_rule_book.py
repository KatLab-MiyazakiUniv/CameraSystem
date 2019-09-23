"""
    @file   test_rule_book.py
    @author T.Miyaji
    @brief  rule_book.pyのテストコード。
"""
from block_bingo_coordinate import BlockCirclesCoordinate
from block_bingo_coordinate import CrossCirclesCoordinate
from rule_book import RuleBook

def create_rule_book(color):
    is_left = True
    bonus = 1
    color = color
    block_circle = BlockCirclesCoordinate(is_left, bonus, color)
    cross_circle = CrossCirclesCoordinate()

    return RuleBook(block_circle, cross_circle)


def test_single_bingo():
    for color in range(1, 8+1):
        rule_book = create_rule_book(color)
        assert color not in rule_book.single_bingo()
        assert 2 == len(rule_book.single_bingo())


def test_double_bingo():
    for color in range(1, 8+1):
        rule_book = create_rule_book(color)
        assert color not in rule_book.double_bingo()
        assert 4 == len(rule_book.double_bingo())