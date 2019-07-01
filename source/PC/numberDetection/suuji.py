#!/usr/bin/env python
#coding: utf-8

import cv2
import numpy as np
import train_mnist
from chainer import Chain, serializers
import chainer.functions  as F
import chainer.links as L
import chainer

def preprocessing(img):
    #中央部分の切り抜き
    # y座標の範囲, x座標の範囲
    img = img[405:652, 50:351]
    cv2.imwrite("img_ori.jpg",img)
    #グレースケールへの変換
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #画像を28x28に縮小
    img = cv2.resize(img, (28, 28))
    cv2.imwrite("img.jpg",img)
    #以下、学習時と同じ処理を行う
    img = 255 - img
    img = img.astype(np.float32)
    img /= 255
    img = np.array(img).reshape(1,784)
    return img

def main():
    # 学習済みモデルの読み込み
    net = L.Classifier(train_mnist.MLP(100, 10))
    serializers.load_npz('source/PC/numberDetection/my_model.npz', net)  ###追加部分###
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(net)
    # Raspberry Pi3（カメラシステム）のURL
    url = "http://192.168.11.25/?action=stream"

    #Webカメラの映像表示
    capture = cv2.VideoCapture(url)
    if capture.isOpened() is False:
            raise("IO Error")
    while True:
        #Webカメラの映像とりこみ
        ret, image = capture.read()
        if ret == False:
            continue
        #Webカメラの映像表示
        cv2.imshow("Capture", image)
        k = cv2.waitKey(10)
        #Eキーで処理実行
        if k == 101:
            print("start")
            img = preprocessing(image)
            num = net.predictor(img)###追加部分###
            print(np.argmax(num.data))###追加部分###
        #ESCキーでキャプチャー画面を閉じる
        if  k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()