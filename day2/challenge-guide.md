---
layout: default
title: "コンテスト課題"
parent: "2日目"
nav_order: 20
---

# コンテスト課題：宝探しゲーム

## 課題概要

toioキューブを操作して，マット上に隠された「宝」を見つけるプログラムを作成する．

宝の位置はランダムに決まり，プログラムを実行するたびに変わる．宝までの「距離情報」を使って，LEDや音でヒントを出しながら宝を探す．

---

## ゲームルール

### 重要: PC画面で宝の距離（位置）の確認禁止

**ゲーム中は，プログラム内で`print(game.get_treasure_distance(cube))`などで宝との距離を直接表示してはいけない．**

代わりに，以下の方法で距離情報を判断する：

- **LEDの色**で距離を表現する（例：赤＝とても近い，オレンジ＝近い）
- **音の高さ・頻度**で距離を表現する（例：高い音＝近い，低い音＝遠い）

---

## ミッション

### 必須課題

1. **キーボード操作**: パターン1のキーボード操作でtoioを動かす
2. **距離情報の取得**: 宝までの距離レベルを取得する
3. **LED制御**: 距離に応じてLEDの色を変える
4. **音制御**: 距離に応じて音を鳴らす
5. **宝の取得**: 宝に近づいたらスペースキーで取得する

### 発展課題（チャレンジ）

- 宝取得時の演出を工夫する（LED点滅，複数の音など）
- パターン2のキーボード操作でtoioを動かす
- toioの移動にキーボード操作を使用せず，自動で宝の近くまで移動するプログラムを作る．

---

## 提供されるファイル

### `treasure_hunt_game.py` - 宝探しゲームクラス

このモジュールには，宝探しに必要なクラスが用意されている．

```python
from treasure_hunt_game import TreasureHuntGame
```

**主なメソッド:**

- `initialize_treasures(num_treasures)`: 宝を配置する（個数を指定可能）
- `get_treasure_distance(cube)`: 最も近い宝までの距離（実数）を返す
- `try_collect_treasure(cube)`: 宝の取得を試みる（全て取得すると自動的にゲーム終了）
- `get_remaining_treasures()`: 残りの宝の数を返す

---

## 距離について

`get_treasure_distance(cube)`は，宝までの距離を **実数** で返す：

| 距離の範囲    | 意味    | 説明                                                     |
| -------- | ----- | ------------------------------------------------------ |
| 0 ～ 15   | とても近い | **この範囲で`try_collect_treasure(cube)`メソッドを実行すると宝を取得できる** |
| 15 ～ 60  | 近い    | もう少し近づく必要がある                                           |
| 60 ～ 100 | 遠い    | まだ遠い                                                   |
| 100以上    | とても遠い | かなり遠い                                                  |

### 距離レベルの視覚化

以下は距離が変わるにつれて，どのようにLED色と音を変えるかの例である：

```
距離: 5      ████████████████████  [赤]         [高い音]
距離: 25     ██████████            [オレンジ]     [中程度の音]
距離: 75     ████                  [緑]         [低めの音]
距離: 150    ██                    [青]         [音なし]
```

**プログラムの工夫**:

距離の値に応じてLEDの色や音を変えることで，宝の方向を探しやすくなる．距離が小さいほど，より目立つLED色（赤など）や，より高い音を出すと効果的である．

---

## TreasureHuntGameクラスの使い方

### 1. ゲームの初期化

```python
from treasure_hunt_game import TreasureHuntGame

game = TreasureHuntGame()
game.initialize_treasures(num_treasures=3)  # ゲーム開始時刻を自動記録
```

**`initialize_treasures(num_treasures)`**

- 引数：宝の個数（1, 3, 5など）
- 動作：マット上にランダムに宝を配置し，ゲーム開始時刻を自動記録
- 戻り値：なし

### 2. 距離情報の取得

```python
distance = game.get_treasure_distance(cube)

if distance is not None:
    print(f"宝までの距離: {distance}")
else:
    print("マット上に宝が配置されていません")
```

**`get_treasure_distance(cube)`**

- 戻り値：最も近い宝までの距離（小数値）
- **注意**：マット外にいるか宝がない場合は`None`を返す
- ゲーム本番はこの値を直接PC画面に表示することは禁止
  - この値を元にLED色や音の高さを変えて，どのくらい近いか判断する

### 3. 宝の取得

```python
success = game.try_collect_treasure(cube)

if success:
    print("宝を取得しました！")
    # 発見時の演出（LED点滅，音など）
else:
    print("この位置では宝を取得できません")
```

**`try_collect_treasure(cube)`**

- 戻り値：成功時は`True`，失敗時は`False`
- 動作：宝の取得範囲内にいる場合，宝を取得
- **自動的にゲーム終了処理**：全ての宝を取得すると，自動的にゲーム終了時刻を記録し表示

### 4. 残りの宝の数の確認

```python
remaining = game.get_remaining_treasures()

if remaining == 0:
    print("全ての宝を取得しました！")
    break  # ゲーム終了
else:
    print(f"あと{remaining}個の宝があります")
```

**`get_remaining_treasures()`**

- 戻り値：残りの宝の個数
- 用途：全ての宝を取得したかの確認

---

## プログラムの流れ（ステップバイステップ）

### ステップ1: キーボード管理の準備

- グローバル変数（`current_keys`, `should_exit`）を定義
- キーボード入力のコールバック関数（`on_press`, `on_release`）を定義
- キーボードリスナーを設定して開始

### ステップ2: ゲーム初期化と実行

toio接続後，以下の処理を実行：

1. TreasureHuntGameを初期化
2. `initialize_treasures()`で宝をマットに配置
3. メインループで以下を繰り返す：
   - キーボード入力から矢印キーの状態を確認
   - 矢印キーに応じてtoioを移動（move，spin，stop）
   - `get_treasure_distance()`で宝までの距離を取得
   - 距離に応じてLED色と音を変更
   - スペースキーが押されたら`try_collect_treasure()`で宝の取得を試みる
   - 全ての宝を取得したら終了

### ステップ3: クリーンアップ

- モーター停止，LED消灯
- キーボードリスナーの停止

---

## プログラムの骨組み（TODO形式）

以下のコード骨組みを参考に，**コメントで示されたTODO部分を自分で埋めて**プログラムを完成させてください．

### ステップ1: 準備（セットアップ部分）

```python
from toio.simple import SimpleCube
from treasure_hunt_game import TreasureHuntGame
from pynput import keyboard
from pynput.keyboard import KeyCode

# キーボード入力の状態管理
current_keys = set()
should_exit = False

def on_press(key):
    global should_exit
    # TODO 1: qキーで終了フラグを設定する
    # TODO 2: キーをcurrent_keysに追加する
    pass

def on_release(key):
    # TODO 3: キーをcurrent_keysから削除する
    pass

target_cube_name = "toio-xxx"

# TODO 4: キーボードリスナーを設定して開始する（listener.start()）
```

### ステップ2: ゲーム初期化と実行（メインループ）

```python
with SimpleCube(name=target_cube_name) as cube:
    # TODO 5: TreasureHuntGameを初期化し，initialize_treasures()で宝を配置する

    while not should_exit:
        # TODO 6: キーボード入力に応じてtoioを移動する
        # 上矢印: move(30, 0) / 下矢印: move(-30, 0)
        # 左矢印: spin(-30, 0) / 右矢印: spin(30, 0)
        # どのキーも押されていない場合: stop_motor()

        # TODO 7: 宝までの距離を取得する（get_treasure_distance()）
        distance = None  # ← ここを修正する

        # TODO 8: 距離に応じてLED色と音を変更する
        # 距離テーブルを参照して実装する

        # TODO 9: スペースキーが押されたときに宝の取得を試みる
        # try_collect_treasure()で取得を試みる
        # 成功したら発見時の演出を実装する
        # get_remaining_treasures() == 0で全て取得済みなら終了する

        cube.sleep(0.01)

    cube.stop_motor()
    cube.turn_off_cube_lamp()

# TODO 10: キーボードリスナーを停止する（listener.stop()）
```

**ヒント**: 各TODO番号は上記の順序で実装します．上から順番に実装していくと，プログラムが完成します．
