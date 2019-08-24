import pytest
from DetectionNumber import DetectionNumber
import cv2

model_path = './DetectionNumber/my_model.npz'


def create_detection(number=None):
    if number is None:
        dn = DetectionNumber(model_path=model_path)
        return dn
    if 1 <= number <= 8:
        img = cv2.imread(f"./DetectionNumber/training_scripts/original/{number}.jpg")
        dn = DetectionNumber(img, model_path=model_path)
        return dn
    raise ValueError("1から8までの数字しかない！")


def test_detection():
    # 1~8までの数字をテスト
    for i in range(1, 9):
        dn = create_detection(i)
        assert dn.get_detect_number() == i


def test_file_not_found_raise():
    dn = create_detection()
    with pytest.raises(FileNotFoundError):
        dn.get_detect_number()


def test_set_img():
    dn = create_detection()
    img = cv2.imread("./DetectionNumber/training_scripts/original/1.jpg")
    dn.set_img(img)
    assert dn.get_detect_number(1)
