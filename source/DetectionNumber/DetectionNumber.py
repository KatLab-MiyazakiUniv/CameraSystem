#!/usr/bin/env python
# coding: utf-8

"""
@file: DetectionNumber.py
@author: korosuke613
@brief: 数字カードを認識する
"""

import cv2
import numpy as np
from MLP import MLP
from chainer import Chain, serializers
import chainer.links as L
import chainer


class DetectionNumber:
    def __init__(self, img=None, model_path='my_model.npz'):
        self.origin_img = img
        self.preprocess_img = None
        self.detected_number = None
        self.number_model_path = model_path
        self.net = L.Classifier(MLP(1000, 10))
        self.data_directory = "data"
        self.img_directory = "imgs"  # 画像を保管するディレクトリ
        self.setup()

    def setup(self):
        # 学習済みモデルの読み込み
        serializers.load_npz(self.number_model_path, self.net)
        optimizer = chainer.optimizers.Adam()
        optimizer.setup(self.net)

    def _preprocessing(self, is_save=False):
        if self.origin_img is None:
            raise FileNotFoundError('数字画像が指定されていません')
        img = cv2.cvtColor(self.origin_img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        # 画像を28x28に縮小
        img = cv2.resize(img, (28, 28))
        if is_save:
            cv2.imwrite("./imgs/preprocess.jpg", img)
        img = img.astype(np.float32)
        img = np.array(img).reshape(1, 784)
        self.preprocess_img = img

    def set_img(self, img):
        self.origin_img = img

    def get_detect_number(self, is_save=False):
        self._preprocessing(is_save)
        num = self.net.predictor(self.preprocess_img)
        return np.argmax(num.data) + 1


def main():
    # Webカメラの映像とりこみ
    img = cv2.imread("./imgs/sample_number.jpg")
    detection_number = DetectionNumber(img)
    number = detection_number.get_detect_number(is_save=True)
    print(number)


if __name__ == '__main__':
    main()
