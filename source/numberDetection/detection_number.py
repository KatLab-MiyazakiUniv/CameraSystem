#!/usr/bin/env python
# coding: utf-8

"""
@file: detection_number.py
@author: korosuke613
@brief: 数字カードを認識する
"""

import cv2
import numpy as np
from MLP import MLP
from chainer import Chain, serializers
import chainer.functions as F
import chainer.links as L
import chainer
import glob
import os
from clipping_number import clipNumber, captureImage

data_directory = "data"
imgs_directory = "imgs"  # 画像を保管するディレクトリ


def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    # 画像を28x28に縮小
    img = cv2.resize(img, (28, 28))
    cv2.imwrite("preprocess.jpg", img)
    img = img.astype(np.float32)
    img = np.array(img).reshape(1, 784)
    return img


def get_image():
    # ラズパイから映像を受信し、保存する
    src_name = captureImage(target_dir=imgs_directory)
    target_name = "_result_" + src_name  # 切り取った画像の出力ファイル名

    # 画像を切り取り、保存する
    clipNumber(src_path=os.path.join(imgs_directory, src_name), target_name=target_name, target_dir=imgs_directory)
    img = cv2.imread(imgs_directory + target_name)
    return img


def get_detect_number(img):
    # 学習済みモデルの読み込み
    net = L.Classifier(MLP(1000, 10))
    serializers.load_npz('my_model.npz', net)
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(net)
    num = net.predictor(img)
    return np.argmax(num.data) + 1


def main():
    # Webカメラの映像とりこみ
    img = get_image()
    img = preprocessing(img)
    number = get_detect_number(img)
    print(number)


if __name__ == '__main__':
    main()
