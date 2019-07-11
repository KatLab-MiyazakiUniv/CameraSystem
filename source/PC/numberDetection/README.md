# 数字認識

## Usage

**プロジェクトルートで実行してください**

### データセット作成

先に、データセットを作成する必要があります。

```bash
pipenv run createNumberData
```

### 学習

次に、学習をおこない、モデルを作成する必要があります。

```bash
pipenv run trainNumber
```

すると、`source/PC/numberDetection/my_model.npz`ができます。

次に、認識を行います。

```bash
pipenv run detectNumber
```

実行すると、カメラ画像を取得し、予測した数字をコンソールに出力します。
