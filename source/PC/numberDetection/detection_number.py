#!/usr/bin/env python
#coding: utf-8

import cv2
import numpy as np
import train_mnist
from chainer import Chain, serializers
import chainer.functions  as F
import chainer.links as L
import chainer
import glob
from clipping_number import clipNumber, captureImage

def preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    #画像を28x28に縮小
    img = cv2.resize(img, (28, 28))
    cv2.imwrite("preprocess.jpg", img)
    img = img.astype(np.float32)
    img = np.array(img).reshape(1, 784)
    return img

def test_model(net):
    def preprocessing_local(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.astype(np.float32)
        img = np.array(img).reshape(1, 784)
        return img
    image_list = glob.glob("source/PC/numberDetection/data/test/images/*")
    result = 0
    for im in image_list:
        image = cv2.imread(im)
        img = preprocessing_local(image)
        num = net.predictor(img)
        correct = im[len("source/PC/numberDetection/data/test/images/"):len("source/PC/numberDetection/data/test/images/") + 1]
        actual = str(np.argmax(num.data) + 1)

        if correct == actual:
            result += 1
        print(correct, actual)###追加部分###

    print("正解は", result)
    return

def get_image():
    imgs_dir = "source/PC/numberDetection/imgs/" # 画像を保管するディレクトリ

    # ラズパイから映像を受信し、保存する
    src_name = captureImage(target_dir=imgs_dir)
    target_name = "_result_" + src_name # 切り取った画像の出力ファイル名
    
    # 画像を切り取り、保存する
    clipNumber(src_path=imgs_dir + src_name, target_name=target_name, target_dir=imgs_dir)
    img = cv2.imread(imgs_dir + target_name)
    return img


def main():
    # 学習済みモデルの読み込み
    net = L.Classifier(train_mnist.MLP(1000, 10))
    serializers.load_npz('source/PC/numberDetection/my_model.npz', net)  ###追加部分###
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(net)
    #Webカメラの映像表示
    #Eキーで処理実行
    print("start")
    #Webカメラの映像とりこみ
    img = get_image()
    img = preprocessing(img)
    num = net.predictor(img)
    print(np.argmax(num.data)+1)
    



if __name__ == '__main__':
    main()