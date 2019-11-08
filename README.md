# CameraSystem
ETロボコン2019のカメラシステムを管理するリポジトリ

[![GitHub Actions](https://github.com/KatLab-MiyazakiUniv/CameraSystem/workflows/Pytest%20and%20Report%20coverage/badge.svg)](https://github.com/KatLab-MiyazakiUniv/CameraSystem/actions) [![CircleCI](https://circleci.com/gh/KatLab-MiyazakiUniv/CameraSystem.svg?style=svg)](https://circleci.com/gh/KatLab-MiyazakiUniv/CameraSystem) [![codecov](https://codecov.io/gh/KatLab-MiyazakiUniv/CameraSystem/branch/master/graph/badge.svg)](https://codecov.io/gh/KatLab-MiyazakiUniv/CameraSystem) [![Coverage Status](https://coveralls.io/repos/github/KatLab-MiyazakiUniv/CameraSystem/badge.svg?branch=master)](https://coveralls.io/github/KatLab-MiyazakiUniv/CameraSystem?branch=master) 

## Setup
Python3.7以上をインストールしておいてください。

### 1. Install Poetry
*Poetry*をインストールします。

```bash
$ pip3 install poetry
```

`pip3` or `pip`

### 2. Creating virtual environment
Python3.7の仮想環境を作ってあげます。

```bash
$ python3.7 -m venv .venv
```

`python3.7` or `python3` or `python`


### 3. Install dependency library
依存ライブラリをインストールします。

```bash
$ poetry install
```

## Testing

```bash
$ ./pytest.sh
```

## With PyCharm
PyCharmで楽しみたい人はこの[URL](https://github.com/KatLab-MiyazakiUniv/CameraSystem/wiki/Pycharm-with-Poerty)を参照


## HOW TO
- `CameraSystem.py`を実行後，以下の表示になったら
- <kbd>d</kbd>を入力すると`DEBUG MODE`
- <kbd>y</kbd>を入力すると`HONBAN MODE`
```bash
SYS: Connect EV3
BT: ちょいまちこ
SYS: 本番ですか？
     y: 本番モード
     d: デバッグモードで実行
>> 
```

#### DEBUG MODE
- 数字カードの四隅をクリック（カメラ画像のウィンドウが後ろに出てるかもしれません）
- 適当なキーボードを入力
- ブロックビンゴエリアの四隅をクリック
- 適当なキーボードを入力
- 交点サークルをドラッグ・アンド・ドロップで囲む
- ブロックサークルをドラッグ・アンド・ドロップで囲む
- 適当なキーボードを入力
- `tkinter`が起動する
- マウスで円を操作し，座標を修正する
- <kbd>d</kbd>を押すと現在の座標をすべてコンソール上に出す
- <kbd>q</kbd>を押すと`tkinter`を終了する
- **ここから下は後で書きます**

#### ATTENTION
##### マウスで円を操作するときの注意
- マウスの動きが早すぎるとだめです
- 円を左クリックした状態で他の円に追突すると暴れます
##### 2回目以降に使う時
- `source`フォルダの中にできる`camera_settings.json`ファイルを削除しないと切り取るモードに入りません