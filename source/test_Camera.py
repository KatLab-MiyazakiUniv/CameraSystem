"""
@file: test_Camera.py
@author: Futa HIRAKOBA
@brief: Camera.pyのをテストするプログラム
"""

from Camera import Camera
import pytest
import cv2


@pytest.fixture()
def camera():
    camera = Camera(url="./img/sample_camera_area.jpg")
    camera.capture(padding=100)
    camera.number_img_range = {
        "l_top": [
            18,
            599
        ],
        "l_btm": [
            226,
            797
        ],
        "r_top": [
            232,
            468
        ],
        "r_btm": [
            488,
            590
        ]
    }
    camera.block_bingo_img_range = {
        "l_top": [
            248,
            390
        ],
        "l_btm": [
            1216,
            767
        ],
        "r_top": [
            739,
            160
        ],
        "r_btm": [
            1348,
            255
        ]
    }
    return camera


def test_clip_number_card(camera):
    img = camera.get_number_img(is_debug=False)
    actual = cv2.imread("./img/sample_number.png")
    assert (img == actual).all()


def test_clip_bingo_area(camera):
    img = camera.get_block_bingo_img(is_debug=False)
    actual = cv2.imread("./img/sample_bingo.png")
    assert (img == actual).all()

