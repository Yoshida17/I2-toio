---
layout: default
title: "マットを使った位置制御"
parent: "2日目"
nav_order: 12
---

# マットを使った位置制御

## 位置制御の基礎

toioマットを使うと，キューブの位置と角度を取得し，目標座標への移動や目標角度への回転ができる．

**位置制御の主な機能**：

1. **`cube.move_to(speed, x, y)`** - 指定座標への移動
2. **`cube.set_orientation(speed, degree)`** - 指定角度への回転
3. **`cube.get_current_position()`** - 現在位置の取得
4. **`cube.get_orientation()`** - 現在角度の取得

まずは簡単な例で動作を確認しよう．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # マットの中心(0, 0)に移動
    cube.move_to(speed=50, x=0, y=0)
```

</details>

---

## 位置制御のAPI

### 指定した座標に移動

```python
success = cube.move_to(speed, x, y)
```

- `speed`: 移動速度（1〜100）
- `x`: 目標のX座標
- `y`: 目標のY座標
- 戻り値: 成功したかどうか（論理型）

**座標系の復習**：

- マット中心が(0, 0)
- X軸：左（負）→ 右（正）
- Y軸：下（負）→ 上（正）

### やってみよう 

**課題1（易）**: キューブを座標(50, 50)に移動させるプログラムを書け．

<details markdown="1">
<summary>ヒント（課題1）</summary>

`cube.move_to(速度, X座標, Y座標)`を使う．速度は30〜70が適切．

</details>

<details markdown="1">
<summary>解答例（課題1）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    success = cube.move_to(speed=50, x=50, y=50)
    if success:
        print("到着しました！")
    else:
        print("移動に失敗しました")
```

</details>

**課題2（中）**: 移動前と移動後の位置をprint文で表示せよ．

<details markdown="1">
<summary>ヒント（課題2）</summary>

`cube.get_current_position()`で現在位置を取得できる．戻り値は`(x, y)`タプルまたは`None`．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    # 移動前の位置
    pos_before = cube.get_current_position()
    if pos_before is not None:
        x, y = pos_before
        print(f"移動前: X = {x}, Y = {y}")

    # 移動
    cube.move_to(speed=50, x=0, y=0)

    # 移動後の位置
    pos_after = cube.get_current_position()
    if pos_after is not None:
        x, y = pos_after
        print(f"移動後: X = {x}, Y = {y}")
```

</details>

**課題3（難）**: 3つの座標を順番に訪問するプログラムを書け：(50, 50) → (-50, 50) → (0, 0)

<details markdown="1">
<summary>ヒント（課題3）</summary>

`cube.move_to()`を3回呼ぶ．各移動の成功・失敗をチェックすると良い．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    points = [[50, 50], [-50, 50], [0, 0]]

    for i, point in enumerate(points):
        x, y = point
        print(f"地点{i+1}: ({x}, {y})へ移動")
        success = cube.move_to(speed=50, x=x, y=y)
        if success:
            print("到着！")
        else:
            print("失敗")
```

</details>

---

### 指定した角度に回転

```python
success = cube.set_orientation(speed, degree)
```

- `speed`: 回転速度（1〜100）
- `degree`: 目標の角度（0〜359）
  - **マイナスで角度を指定できないので注意**
  - 左向き(-90度)にしたい場合は270とする．
- 戻り値: 成功したかどうか（論理型）

**角度の復習**：

- 0度：上向き
- 90度：右向き
- 180度：下向き
- -90度（270度）：左向き

### やってみよう 

**課題1（易）**: キューブを90度（右向き）に回転させるプログラムを書け．

<details markdown="1">
<summary>ヒント（課題1）</summary>

`cube.set_orientation(速度, 角度)`を使う．速度は30〜70が適切．

</details>

<details markdown="1">
<summary>解答例（課題1）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    success = cube.set_orientation(speed=50, degree=90)
    if success:
        print("回転完了！")
```

</details>

**課題2（中）**: 回転前と回転後の角度をprint文で表示せよ．

<details markdown="1">
<summary>ヒント（課題2）</summary>

`cube.get_orientation()`で現在角度を取得できる．戻り値は角度（度）または`None`．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    # 回転前
    angle_before = cube.get_orientation()
    if angle_before is not None:
        print(f"回転前: {angle_before}度")

    # 回転
    cube.set_orientation(speed=50, degree=180)

    # 回転後
    angle_after = cube.get_orientation()
    if angle_after is not None:
        print(f"回転後: {angle_after}度")
```

</details>

**課題3（難）**: 0度 → 90度 → 180度 → -90度 → 0度と順番に回転するプログラムを書け．各回転の間に1秒待機すること．

<details markdown="1">
<summary>ヒント（課題3）</summary>

`cube.set_orientation()`を4回呼ぶ．各回転の後に`cube.sleep(1)`で待機．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    angles = [0, 90, 180, 270, 0]

    for angle in angles:
        print(f"{angle}度に回転")
        cube.set_orientation(speed=50, degree=angle)
        cube.sleep(1)
```

</details>

---

## 四角形を描く

`move_to()`を使って四角形の各頂点を順番に訪問すると，四角形を描くことができる．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    # 四角形の各頂点
    points = [
        [50, 50],    # 右上
        [50, -50],   # 右下
        [-50, -50],  # 左下
        [-50, 50],   # 左上
        [50, 50]     # 最初の位置に戻る
    ]

    for point in points:
        x, y = point
        cube.move_to(speed=30, x=x, y=y)
```

</details>

### やってみよう 

**課題1（易）**: プログラム例を実行し，正しく四角形が描けることを確認せよ．速度を変えて実験せよ．

**課題2（中）**: 三角形を描くプログラムを書け．3つの頂点の座標は自分で決めよ．

<details markdown="1">
<summary>ヒント（課題2）</summary>

三角形なので3つの座標が必要．最後に最初の座標に戻ると完全な三角形になる．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    points = [
        [0, 60],     # 上
        [60, -30],   # 右下
        [-60, -30],  # 左下
        [0, 60]      # 最初に戻る
    ]

    for point in points:
        x, y = point
        cube.move_to(speed=40, x=x, y=y)
```

</details>

**課題3（難）**: 四角形の各頂点で1秒停止し，その間LED色を変えるプログラムを書け（頂点ごとに異なる色）．

<details markdown="1">
<summary>ヒント（課題3）</summary>

各移動の後に`cube.turn_on_cube_lamp(r, g, b, 1)`を入れる．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    points = [[50, 50], [50, -50], [-50, -50], [-50, 50]]
    colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]]

    for i in range(len(points)):
        x, y = points[i]
        r, g, b = colors[i]
        cube.move_to(speed=40, x=x, y=y)
        cube.turn_on_cube_lamp(r, g, b, 1)
```

</details>

---

## 位置情報と条件分岐の組み合わせ

位置情報を繰り返し取得し，現在位置に応じて動作を変えることができる．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    # 10秒間，位置に応じてLED色を変える
    for i in range(20):
        position = cube.get_current_position()

        if position is not None:
            x, y = position

            if x > 0 and y > 0:  # 第1象限（右上）
                cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤
            elif x < 0 and y > 0:  # 第2象限（左上）
                cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑
            elif x < 0 and y < 0:  # 第3象限（左下）
                cube.turn_on_cube_lamp(0, 0, 255, 0.5)  # 青
            elif x > 0 and y < 0:  # 第4象限（右下）
                cube.turn_on_cube_lamp(255, 255, 0, 0.5)  # 黄

        cube.sleep(0.5)
```

</details>

### やってみよう 

**課題1（易）**: プログラム例を実行し，キューブを手で動かして各象限で色が変わることを確認せよ．

**課題2（中）**: マット中心から距離50以内にいる場合は緑色，それ以外は赤色にするプログラムを書け．

<details markdown="1">
<summary>ヒント（課題2）</summary>

距離は`(x**2 + y**2)**0.5`で計算できる．三平方の定理を使う．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    for i in range(20):
        position = cube.get_current_position()

        if position is not None:
            x, y = position
            distance = (x**2 + y**2)**0.5  # 中心からの距離

            if distance < 50:
                cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑
            else:
                cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤

        cube.sleep(0.5)
```

</details>

**課題3（難）**: 角度に応じてLED色を変えるプログラムを書け：

- 0度〜90度：赤
- 90度〜180度：緑
- 180度〜-90度：青
- -90度〜0度：黄

<details markdown="1">
<summary>ヒント（課題3）</summary>

`cube.get_orientation()`で角度を取得し，if-elif文で分岐．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    for i in range(20):
        angle = cube.get_orientation()

        if angle is not None:
            if 0 <= angle < 90:
                cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤
            elif 90 <= angle < 180:
                cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑
            elif angle >= 180 or angle < -90:
                cube.turn_on_cube_lamp(0, 0, 255, 0.5)  # 青
            else:  # -90 <= angle < 0
                cube.turn_on_cube_lamp(255, 255, 0, 0.5)  # 黄

        cube.sleep(0.5)
```

</details>

---

## 総合チャレンジ 🏆

### チャレンジ: 自動パトロール

マットの4隅を順番に巡回し，各地点で360度回転して周囲を「警戒」するプログラムを書け．

<details markdown="1">
<summary>ヒント</summary>

4隅の座標は`[135, 90], [-135, 90], [-135, -90], [135, -90]`など．各地点で`set_orientation()`を使って0度→90度→180度→270度と回転．

</details>

<details markdown="1">
<summary>解答例</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    corners = [[135, 90], [-135, 90], [-135, -90], [135, -90]]
    angles = [0, 90, 180, 270]

    for corner in corners:
        x, y = corner
        print(f"({x}, {y})に移動")
        cube.move_to(speed=50, x=x, y=y)

        # 360度回転して警戒
        for angle in angles:
            cube.set_orientation(speed=60, degree=angle)
            cube.turn_on_cube_lamp(255, 0, 0, 0.3)

        cube.turn_on_cube_lamp(0, 255, 0, 1)  # 緑で安全を示す
        cube.sleep(1)
```

</details>

---

## 移動に失敗する場合のヒント

マット情報の読み取りに失敗する場合は，toioの位置を少しずらして再挑戦する処理を入れる．

```python
while True:
    success = cube.move_to(speed=30, x=target_x, y=target_y)
    if success:
        break  # 移動成功時はループを抜ける
    else:
        print("移動失敗，微調整して再挑戦")
        cube.spin(10, 0.1)  # 0.1秒回転して再挑戦
```
