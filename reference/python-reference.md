---
layout: default
title: "Pythonリファレンス"
parent: "リファレンス"
nav_order: 10
---

# Pythonクイックリファレンス

このページは，toioプログラミングで使用するPython構文のクイックリファレンスである．

**注意**: このページは最小限の説明のみを提供する．Pythonプログラミングの詳細については，並行して受講しているプログラミングの授業を参照すること．

---

## 変数とデータ型

```python
# 変数に値を代入
name = "Tanaka"        # 文字列型（str）
age = 15               # 整数型（int）
speed = 50.5           # 浮動小数点型（float）
is_moving = True       # 論理型（bool）- TrueまたはFalse

# 変数の値を表示
print(name)
print("速度:", speed)
```

**主なデータ型:**
- `str` - 文字列（`"Hello"`, `"こんにちは"`）
- `int` - 整数（`10`, `-5`, `0`）
- `float` - 小数（`3.14`, `-2.5`）
- `bool` - 論理値（`True`, `False`）

---

## 演算子

```python
# 算術演算子
a = 10
b = 3

a + b    # 13 - 足し算
a - b    # 7  - 引き算
a * b    # 30 - 掛け算
a / b    # 3.333... - 割り算（小数）
a // b   # 3  - 割り算（整数部分のみ）
a % b    # 1  - 余り

# 比較演算子
a == b   # False - 等しい
a != b   # True  - 等しくない
a > b    # True  - より大きい
a < b    # False - より小さい
a >= b   # True  - 以上
a <= b   # False - 以下
```

---

## 条件分岐（if文）

```python
# 基本的なif文
if speed > 50:
    print("速すぎます")

# if-else文
if speed > 50:
    print("速すぎます")
else:
    print("適切な速度です")

# if-elif-else文
if speed > 80:
    print("危険な速度です")
elif speed > 50:
    print("速すぎます")
else:
    print("適切な速度です")
```

**重要**: `if`文の後には必ずコロン`:`を付け，実行する内容は**インデント**（字下げ）する．

---

## 繰り返し処理（for文）

```python
# 5回繰り返す
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4 が表示される

# range()の使い方
range(5)        # 0から4まで（0, 1, 2, 3, 4）
range(1, 6)     # 1から5まで（1, 2, 3, 4, 5）
range(0, 10, 2) # 0から8まで2ずつ（0, 2, 4, 6, 8）

# リストの要素を順番に処理
colors = ["red", "green", "blue"]
for color in colors:
    print(color)
```

**ポイント**: `for`文の後にもコロン`:`を付け，繰り返す内容は**インデント**する．

---

## 繰り返し処理（while文）

```python
# 条件が真である間，繰り返す
counter = 0
while counter < 5:
    print(counter)
    counter = counter + 1  # カウンターを増やす
```

**注意**: 無限ループに陥らないように，必ずループ内で条件が偽になるようにする．

---

## リスト

リストは複数の値を順番に格納できるデータ型である．

```python
# リストの作成
numbers = [10, 20, 30, 40, 50]
colors = ["red", "green", "blue"]

# 要素の取得（インデックスは0から始まる）
print(numbers[0])    # 10 - 最初の要素
print(numbers[1])    # 20 - 2番目の要素
print(numbers[-1])   # 50 - 最後の要素

# リストの長さ
print(len(numbers))  # 5

# 要素の追加
colors.append("yellow")

# リストをforループで処理
for num in numbers:
    print(num)
```

---

## インデント（字下げ）

Pythonでは**インデント**がプログラムの構造を決定する．

```python
# 正しいインデント
if True:
    print("これは実行されます")    # インデントされている
    print("これも実行されます")      # 同じインデントレベル

# インデントがないとエラーになる
if True:
print("エラー！")  # インデントがない
```

**Thonnyでのインデント**: `Tab`キーを押すとインデントが追加される．

---

## よく使う関数

```python
# 画面に出力
print("こんにちは")
print("速度:", 50)

# 型変換
int("10")      # 文字列を整数に変換
float("3.14")  # 文字列を浮動小数点数に変換
str(100)       # 数値を文字列に変換

# 数学関数
abs(-10)       # 絶対値: 10
max(1, 5, 3)   # 最大値: 5
min(1, 5, 3)   # 最小値: 1
```

---

## toioプログラミングで特によく使う構文

### 繰り返しパターン

```python
# N回繰り返す
for i in range(3):
    cube.move(50, 1)
    cube.sleep(1.5)

# 条件が満たされるまで繰り返す
while cube.get_x() < 100:
    cube.move(30, 0)
    cube.sleep(0.1)
```

### 条件による動作変更

```python
# 位置に応じて動作を変える
x = cube.get_x()
if x < 0:
    cube.turn_on_cube_lamp(255, 0, 0, 1)  # 赤
elif x < 100:
    cube.turn_on_cube_lamp(0, 255, 0, 1)  # 緑
else:
    cube.turn_on_cube_lamp(0, 0, 255, 1)  # 青
```

### リストを使った制御

```python
# 複数の座標を順番に訪問
positions = [(50, 50), (100, 50), (100, 100), (50, 100)]

for x, y in positions:
    cube.move_to(80, x, y)
    cube.sleep(0.5)
```

---

## 困ったときは

- **インデントエラー**: インデントが正しくない場合に発生．`Tab`キーでインデントを揃える
- **構文エラー**: コロン`:`を忘れていないか確認
- **名前エラー**: 変数名のスペルミスや，定義前の変数を使用していないか確認
- **型エラー**: 数値と文字列を混同していないか確認

詳しい説明やエラーの解決方法については，**プログラミングの授業で学んだ内容を参照**すること．
