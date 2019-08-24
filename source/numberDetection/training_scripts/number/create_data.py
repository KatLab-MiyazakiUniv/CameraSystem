"""
@file: create_data.py
@author: korosuke613
@brief: 画像を大量に生成する
"""

import cv2
import numpy as np
import glob
from tqdm import tqdm, trange
import os
import shutil


def load_original():
    image_list = glob.glob("original/*")
    # 画像の読込(numpy.ndarrayで読み込まれる)
    image_list.sort()
    images = []
    for image_address in image_list:
        images.append(cv2.imread(image_address))
    return images

def binaryzation(image):
    #グレースケールへの変換
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
    #画像を28x28に縮小
    img = cv2.resize(img, (28, 28))
    return img

def getMeanColor(image):
    # RGB平均値を出力
    # flattenで一次元化しmeanで平均を取得 
    b = image.T[0].flatten().mean()
    g = image.T[1].flatten().mean()
    r = image.T[2].flatten().mean()
    return {"r": r, "g": g, "b": b}

def change_angle(image):
    # 中心位置取得
    center = tuple(np.array([image.shape[1] * 0.5, image.shape[0] * 0.5]))

    # 回転させたい角度°(ラジアンではない)
    rand_num = np.random.rand() * 60.0 - 30.0
    angle = rand_num

    # 拡大比率
    rand_num = np.random.rand() * 0.5 - 0.25
    scale = 1.0 + rand_num

    # 回転変換行列の算出![edges.png](https://qiita-image-store.s3.amazonaws.com/0/294506/5d919d71-d994-ab16-28d2-c0217b975ff0.png)

    affine_mat = cv2.getRotationMatrix2D(center, angle, scale)

    # 平均色の取得
    mean =  getMeanColor(image)
    # アフィン変換(回転)
    height, width = image.shape[:2]
    rotation_image = cv2.warpAffine(image, affine_mat, (width, height), flags=cv2.INTER_CUBIC, borderValue=(mean["b"], mean["g"], mean["r"]))

    return rotation_image

def change_brightness(image):
    # 乱数生成
    rand_num = np.random.rand() / 2
    # γ値の定義(1より小さいと暗く、1より大きいと明るくなる)
    gamma = 1 - rand_num

    # ルックアップテーブルの生成
    look_up_table = np.zeros((256, 1), dtype=np.uint8)
    for i in range(256):
        look_up_table[i][0] = 255 * (float(i)/255) ** (1.0 / gamma)

    # γ変換後の画像取得
    image_gamma = cv2.LUT(image, look_up_table)
    return image_gamma


def save_image(image, name, dir_name):
    cv2.imwrite(dir_name + name + ".jpg", image)


def print_image(image):
    # 画像を表示
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def create_labels(dir_name):
    image_list = glob.glob(dir_name + "*")

    label_list = []
    for image in image_list:
        file_name = image[len(dir_name):]
        label = str(int(file_name[:1]) - 1)
        label_list.append(file_name + " " + label)
    
    # ファイルを書き込みモードで開く
    name = dir_name.split("/")[0]
    text = "\n".join(label_list)             # 改行コードでつなぐ
    with open(name + "/" + name + '_labels.txt', 'w') as f:
        # 書き込み
        f.write(text)

def create_dataset(name, iteration=100):
    images = load_original()
    num = ["1", "2", "3", "4", "5", "6", "7", "8"]

    num_key = 0
    dir_name = name + "/images/"
    shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    
    for original_image in tqdm(images, desc='1st loop'):
        for i in trange(iteration, desc='2nd loop'):
            image = change_brightness(original_image)
            image = change_angle(image)
            image = binaryzation(image)
            name = num[num_key] + "_" + str(i)
            save_image(image, name, dir_name)
        num_key += 1
    create_labels(dir_name)

if __name__ == "__main__":
    create_dataset("train", 1000)
    create_dataset("valid", 10)
    create_dataset("test", 300)
