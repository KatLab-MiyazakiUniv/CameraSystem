# CameraSystem
ETロボコン2019のカメラシステムを管理するリポジトリ

[![GitHub Actions](https://github.com/KatLab-MiyazakiUniv/CameraSystem/workflows/Pytest%20and%20Report%20coverage/badge.svg)](https://github.com/KatLab-MiyazakiUniv/CameraSystem/actions) [![codecov](https://codecov.io/gh/KatLab-MiyazakiUniv/CameraSystem/branch/master/graph/badge.svg)](https://codecov.io/gh/KatLab-MiyazakiUniv/CameraSystem)

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
