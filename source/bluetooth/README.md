# 走行体とのBluetooth接続

## 前提条件
- PCにBluetooth機能がある．
- 走行体にBluetooth設定ファイルが入っている．
- 走行体にBluetooth通信をするプログラムが入っている．

## Usage

**プロジェクトルートで実行してください**

### 走行体とPCとのBluetooth接続

先に，走行体とPCをBluetooth接続してください．接続方法は，Bluetoothイヤフォンとかを接続するときの方法と一緒です．

### 走行体と接続しているシリアルポートを探す

Bluetooth通信がどうとか言っていますが結局やっていることは，シリアル通信です．ケーブルの代わりに接続方法がBluetoothに変わっただけだと考えてもらえれば大丈夫です．

そこで，走行体とつながっているシリアルポートを探します．

```bash
pipenv run search_serial_port
```

すると、走行体とつながっているそれっぽい名前のシリアルポートが出てきます．Macの場合は，`/dev/cu.MindstormsEV3`みたいな感じのが出てくると思います．（この名前は，走行体の中に入っている設定ファイルに書いている内容によって変わります．）

### シリアルポートの名前をプログラムに入れる

`Bluetooth`クラスの`connect`メソッドの引数に調べたシリアルポートの名前を渡します．具体的には，`main`関数のところの

```python
bluetooth.connect("/dev/cu.MindstormsEV301-SerialP")
```
を書き換えてください．

### 実行

```bash
pipenv run bluetooth
```
3秒毎に0から9の整数を走行体に送信します．

### 参考サイト
[EV3RTを使ってみる(8)](http://blog.takedarts.jp/2015/04/28/390)
