# 数字認識

## Usage

先に、学習をおこない、モデルを作成する必要があります。

```python
python source/PC/numberDetection/train_mnist.py
```

すると、`source/PC/numberDetection/my_model.npz`ができます。

次に、認識を行います。

```python
python source/PC/numberDetection/suuji.py
```

実行すると、カメラ画像が表示されます。

Eキーを押します。

コンソールに、予測した数字が出ます。