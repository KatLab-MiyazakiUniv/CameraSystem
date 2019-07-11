#!/usr/bin/env python
# coding: utf-8

# 色に関する定義
class Color():
    # 色コード
    UNKNOWN = 0
    RED     = 1
    GREEN   = 2
    BLUE    = 3
    BLACK   = 4
    YELLOW  = 5

    # 色コードから表示用文字列への変換メソッド
    def toColorName(code):
        COLOR_NAME = {
            Color.UNKNOWN: "Unknown",
            Color.RED:     "RED",
            Color.GREEN:   "GREEN",
            Color.BLUE:    "BLUE",
            Color.BLACK:   "BLACK",
            Color.YELLOW:  "YELLOW"
        }
        return COLOR_NAME[code]

    # HSV値から色コードへの変換メソッド(閾値は環境に合わせて調整下さい)
    def getColor(hsv):
        if (0 <= hsv[2] and hsv[2] <= 20):
            return Color.BLACK
        if (0 <= hsv[0] and hsv[0] <= 15) \
            and (20 <= hsv[1] and hsv[1] <= 255) \
            and (20 <= hsv[2] and hsv[2] <= 255):
            return Color.RED
        if (100 <= hsv[0] and hsv[0] <= 115) \
            and (60 <= hsv[1] and hsv[1] <= 255) \
            and (60 <= hsv[2] and hsv[2] <= 255):
            return Color.BLUE
        if (45 <= hsv[0] and hsv[0] <= 90) \
            and (50 <= hsv[1] and hsv[1] <= 255) \
            and (50 <= hsv[2] and hsv[2] <= 255):
            return Color.GREEN
        if (20 <= hsv[0] and hsv[0] <= 30) \
            and (20 <= hsv[1] and hsv[1] <= 255) \
            and (20 <= hsv[2] and hsv[2] <= 255):
            return Color.YELLOW
        return Color.UNKNOWN

# コマンドコード定義
class CommandCode():
    Specific = 0x01
    All      = 0x02

# レスポンスコード定義
class ResponseCode():
    Color = 0x51
    Error = 0xC8
    