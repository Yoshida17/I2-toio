---
layout: default
title: "モーター制御"
parent: "1日目"
nav_order: 30
---

# モーター制御の基本

## モーター制御の基礎

toioキューブには3つの基本的なモーター制御APIがある：

1. **`cube.move(speed, duration)`** - 前進・後退
2. **`cube.spin(speed, duration)`** - その場で回転
3. **`cube.run_motor(left, right, duration)`** - 左右モーター個別制御

まずは簡単な例で動作を確認しよう．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    cube.move(30, 1)  # 速度30で1秒間前進
```

</details>

---

## モーター制御のAPI

### 前後移動

```python
cube.move(speed, duration)
```

- `speed`: 速度（-100〜100）．正の値で前進，負の値で後退
- `duration`: 動作時間（秒）．最大2.55秒．0を入力した場合は制限時間なし．

### duration=0の使い方

`duration=0`にすると，モーターは停止命令を受けるまで動き続ける．これにより，移動しながら他の処理（LED制御や音再生など）を同時に実行できる．

**duration=0を使わない場合**：

```python
cube.move(30, 2)  # 2秒間前進（この間は他の処理ができない）
cube.turn_on_cube_lamp(255, 0, 0, 1)  # 前進が終わってから光る
```

**duration=0を使う場合**：

```python
cube.move(30, 0)  # 前進開始（すぐ次の処理へ）
cube.turn_on_cube_lamp(255, 0, 0, 1)  # 前進しながら光る
cube.sleep(2)     # 2秒待つ
cube.stop_motor() # 停止
```

**重要**: `duration=0`を使った場合，プログラムが終了すると自動的にモーターも停止する．明示的に停止したい場合は`cube.stop_motor()`を使う．

---

## 待機と停止のAPI

### 指定時間待機する

```python
cube.sleep(seconds)
```

- `seconds`: 待機時間（秒）

**重要**: Pythonの `time.sleep()` の代わりに `cube.sleep()` を使用する． `time.sleep()` を使うとキューブとの通信が途切れることがある．

### モーターを停止する

```python
cube.stop_motor()
```

---

### やってみよう 

**課題1（易）**: 速度を20, 50, 100に変えて実行し，動きの違いを観察せよ．

**課題2（中）**: 負の速度（-50）で実行せよ．何が起こるか？

**課題3（難）**: 以下の動きをするプログラムを**自分で**書け：

- 2秒前進 → 1秒停止 → 2秒後退

<details markdown="1">
<summary>ヒント（課題3）</summary>

- sleepには `cube.sleep()` を使う
- `duration=0`を使った場合，停止するには `cube.stop_motor()` を使う

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    cube.move(50, 2)      # 2秒前進
    cube.sleep(1)         # 1秒待つ
    cube.move(-50, 2)     # 2秒後退
```

</details>

### その場で回転

```python
cube.spin(speed, duration)
```

- `speed`: 速度（-100〜100）．正の値で時計回り，負の値で反時計回り
- `duration`: 動作時間（秒）．最大2.55秒．0を入力した場合は制限時間なし．

### やってみよう 

**課題1（易）**: 正の速度（50）と負の速度（-50）を試して，回転方向の違いを確認せよ．

**課題2（中）**: 速度20で何秒間回転させると，ちょうど90度（直角）回転するか実験で調べよ．

**課題3（難）**: 以下の動きをするプログラムを**自分で**書け：

- 1秒前進 → 90度左回転 → 1秒前進 → 90度左回転（これを4回繰り返して正方形を描く）

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `for i in range(4):` で4回繰り返す
- 左回転は負の速度(-20)を使う
- 課題2で調べた時間を使う

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    for i in range(4):
        cube.move(50, 1)      # 1秒前進
        cube.spin(-20, 0.5)   # 90度左回転（時間は実験で調整）
```

**注意**: 回転時間は環境によって異なるため，実際に試して調整する必要がある．

</details>

### 左右のモーターを個別に制御

```python
cube.run_motor(left_speed, right_speed, duration)
```

- `left_speed`: 左モーターの速度（-100〜100）
- `right_speed`: 右モーターの速度（-100〜100）
- `duration`: 動作時間（秒）．最大2.55秒．0を入力した場合は制限時間なし．

### やってみよう 

**課題1（易）**: `run_motor(50, 50, 2)` を実行せよ．`move(50, 2)` と何が違うか？

**課題2（中）**: 以下のパラメータで実行し，動きを観察せよ：

- `run_motor(70, 30, 2)` - どちらに曲がる？
- `run_motor(30, 70, 2)` - どちらに曲がる？
- `run_motor(50, -50, 2)` - どう動く？

**課題3（難）**: 8の字を描くプログラムを**自分で**書け．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- 8の字 = 右カーブで円 + 左カーブで円
- 右カーブ：左モーター速度 > 右モーター速度
- 左カーブ：右モーター速度 > 左モーター速度
- 速度差を大きくすると，カーブがきつくなる

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    # 右回りの円（左が速い）
    cube.run_motor(60, 30, 3)
    cube.sleep(0.5)
    # 左回りの円（右が速い）
    cube.run_motor(30, 60, 3)
```

**注意**: 速度と時間は実験で調整する必要がある．

</details>

---

## プログラム例：カーブと回転

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # 左右のモーターを別々に動かす（左：70，右：30で2秒間）
    cube.run_motor(70, 30, 2)  # 右カーブしながら前進

    # 1秒待つ
    cube.sleep(1)

    # 反対側に曲がる（左：30，右：70で2秒間）
    cube.run_motor(30, 70, 2)  # 左カーブしながら前進

    # その場で回転（左：50，右：-50で2秒間）
    cube.run_motor(50, -50, 2)  # その場で左回転
```

</details>

---



## 総合チャレンジ 🏆

ここまで学んだモーター制御APIを組み合わせて，以下の課題に挑戦しよう．

### チャレンジ1：ジグザグ走行

以下の動きをするプログラムを書け：

1. 2秒前進
2. 90度右回転
3. 1秒前進
4. 90度左回転
5. 2秒前進

<details markdown="1">
<summary>ヒント</summary>

- `move()` と `spin()` を組み合わせる
- 右回転は正の速度，左回転は負の速度

</details>

### チャレンジ2：円を描く

`run_motor()` を使って，できるだけ綺麗な円を描くプログラムを書け．

<details markdown="1">
<summary>ヒント</summary>

- 左右のモーター速度の**差**を一定に保つ
- 速度差が小さいほど大きな円になる
- 実験して最適な速度と時間を見つける

</details>
