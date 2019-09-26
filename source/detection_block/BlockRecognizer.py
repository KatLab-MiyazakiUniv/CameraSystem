from BlockBingo import BlockBingo
from BlockBingo import Color
import cv2
import numpy as np

class BlockRecognizer:
    def __init__(self):
        self.block_bingo = BlockBingo()
        self.extractor = BlockExtractor()
                      
    def convert_to_hsv(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h = hsv.T[0].flatten().mean()
        s = hsv.T[1].flatten().mean()
        v = hsv.T[2].flatten().mean()
        return (h, s, v)
        
    def detect_color(self, img):        
        # 各色のHue最小値と最大値
        hue_list = {Color.RED:[0, 15], Color.BLUE:[90, 110],
                      Color.YELLO:[15, 30], Color.GREEN:[60, 90]}
        (h, s, v) = self.convert_to_hsv(img)
        
        # 黒色の識別
        if 0 <= v < 40:
            return Color.BLACK
        # 白色の識別
        if 240 <= v < 256:
            return Color.WHITE

        for (key, value) in hue_list.items():
            if value[0] <= h < value[1]:
                return key
        print(h, s, v)
        return None
        
    def recognize_block_circle(self, img, points):
        img = self.extractor.remove_circle_number(img)
        black = None
        for (idx, point) in enumerate(points):
            crop = self.extractor.trim(img, point)
            if Color.BLACK == self.detect_color(self.extractor.closing(crop)):
                black = idx + 1
        
        return black      

class BlockExtractor():
    def trim(self, img, point, margin = 5):
        """
        画像を指定の座標周辺で切り取る。
        
        Parameters
        ----------
        img : Mat
            画像
        point : tuple
            座標
        margin : int
            指定座標の周囲(px)
        """
        return img[point[1]-margin:point[1]+margin, point[0]-margin:point[0]+margin]

    def hsv_decomposition(self, img):
        """
        HSV分解する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return cv2.split(hsv)

    def binarization(self, img):
        """
        2値化処理する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        (h, s, v) = self.hsv_decomposition(img)
        s = cv2.GaussianBlur(s, (19,19), 0)
        _, dst = cv2.threshold(s, 57, 255, cv2.THRESH_BINARY)
        return dst

    def closing(self, img):
        """
        クロージング処理する。
        
        Parameters
        ----------
        img : Mat
            画像
        """
        # 8近傍の定義
        kernel = np.ones((9,9))
        mask = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return mask
    
    def opening(self, img):
        """
        オープニング処理する。
                
        Parameters
        ----------
        img : Mat
            画像
        """
        # 8近傍の定義
        kernel = np.ones((9,9))
        mask = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return mask

    def remove_circle_number(self, img):
        """
        ブロックサークルの数字を削除する。画像の周辺のノイズも削除する
                
        Parameters
        ----------
        img : Mat
            画像
        """
        # 2値化処理
        mask = self.binarization(img)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # マスク処理をして画像から不要な情報を削除する
        dst = cv2.bitwise_and(img, mask)
        # 不要な情報が黒色になっているので白色に変換する
        return cv2.addWeighted(dst, 1, cv2.bitwise_not(mask), 1, 0)

if __name__ == '__main__':
    img = cv2.imread('result.png')
    recognizer = BlockRecognizer()
    points = [ (130, 151), (311, 152), (493, 152), (127, 345), (483, 331), (126, 537), (305, 532), (480, 534)]
    print(recognizer.recognize_block_circle(img, points))
