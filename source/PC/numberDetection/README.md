# 数字認識

## Usage

### データセット作成
先に、データセットを作成する必要があります。

```bash
cd source/PC/numberDetection/data
python create_data.py
```

### 学習

次に、学習をおこない、モデルを作成する必要があります。

```bash
python source/PC/numberDetection/train_mnist.py
```

すると、`source/PC/numberDetection/my_model.npz`ができます。

次に、認識を行います。

```bash
python source/PC/numberDetection/suuji.py
```

実行すると、カメラ画像を取得し、予測した数字をコンソールに出力します。
