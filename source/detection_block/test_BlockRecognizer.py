import cv2

from BlockRecognizer import BlockRecognizer
from BlockBingo import Color

def create_block_recognizer():
    bonus = 1
    is_Left = True
    return BlockRecognizer(bonus, is_Left)


def test_result():
    circles_coordinates = {
        'c00': (34, 61), 'c10': (210, 61), 'c20': (393, 56), 'c30': (573, 58),
        "b1": (122, 153), "b2": (302, 155), "b3": (480, 150),
        'c01': (36, 243), 'c11': (217, 242), 'c21': (392, 243), 'c31': (577, 241),
        "b4": (127, 338), "b5": (480, 339),
        'c02': (43, 425), 'c12': (219, 429), 'c22': (399, 426), 'c32': (572, 427),
        "b6": (130, 521), "b7": (307, 521), "b8": (481, 520),
        'c03': (49, 608), 'c13': (227, 606), 'c23': (400, 607), 'c33': (578, 608)
        }
    
    recognizer = create_block_recognizer()
    img = cv2.imread('result.png')
    bc, cc = recognizer.recognize(img, circles_coordinates)

    # 正解データ result_cc_blocks[col][row]
    result_cc_blocks = (
        (Color.BLUE, Color.WHITE, Color.RED, Color.WHITE),
        (Color.WHITE, Color.GREEN, Color.WHITE, Color.BLACK),
        (Color.BLUE, Color.WHITE, Color.YELLOW, Color.WHITE),
        (Color.WHITE, Color.YELLOW, Color.WHITE, Color.GREEN)
        )
    
    assert (5, 7) == (bc.get_black_circle(), bc.get_color_circle())
    for row in range(4):
        for col in range(4):
            assert cc.cross_circles[col][row] == result_cc_blocks[col][row]
    

def test_result1():
    circles_coordinates = {
        'c00': (43, 48), 'c10': (217, 50), 'c20': (398, 47), 'c30': (576, 48),
        "b1": (130, 145), "b2": (304, 148), "b3": (487, 147),
        'c01': (42, 232), 'c11': (222, 237), 'c21': (396, 236), 'c31': (578, 235),
        "b4": (131, 331), "b5": (484, 333),
        'c02': (46, 420), 'c12': (222, 422), 'c22': (402, 418), 'c32': (571, 419),
        "b6": (133, 517), "b7": (311, 517), "b8": (483, 515),
        'c03': (52, 606), 'c13': (231, 604), 'c23': (399, 608), 'c33': (581, 607)}

    recognizer = create_block_recognizer()
    img = cv2.imread('result1.png')
    bc, cc = recognizer.recognize(img, circles_coordinates)
    
    # 正解データ result1_cc_blocks[col][row]
    result1_cc_blocks = (
        (Color.BLUE, Color.WHITE, Color.RED, Color.WHITE),
        (Color.WHITE, Color.YELLOW, Color.WHITE, Color.BLACK),
        (Color.BLUE, Color.WHITE, Color.RED, Color.WHITE),
        (Color.WHITE, Color.YELLOW, Color.WHITE, Color.GREEN)
        )
    
    assert (5, 2) == (bc.get_black_circle(), bc.get_color_circle())
    for row in range(4):
        for col in range(4):
            assert cc.cross_circles[col][row] == result1_cc_blocks[col][row]
