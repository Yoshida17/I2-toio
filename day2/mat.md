---
layout: default
title: "位置情報の取得"
parent: "2日目"
nav_order: 11
---

# 位置情報と角度情報の取得（マット使用）

## 位置情報の基礎

toioマットを使うと，キューブの位置（x, y座標）と角度（向き）を取得できる．これにより，精密な移動制御が可能になる．

### なぜ位置情報が必要か？

1日目では，`move()`や`spin()`を使ってキューブを動かしていた．これらのAPIは「前に進む」「回転する」といった**相対的な動き**を制御するものである．

しかし，より高度なプログラムを作成するには，「現在どこにいるのか」「どの方向を向いているのか」といった**絶対的な位置情報**が必要になる．例えば：

- 「マットの四隅を順番に訪問する」
- 「指定された座標に正確に移動する」
- 「目標座標の方向に正確に向き直す」

こうした処理には，位置情報を取得・活用する仕組みが不可欠である．

### マットの座標系

toioマットの座標系は以下のように定義されている：

- **原点**: マットの中心が (0, 0)
- **X軸**: 右が正の方向（右に進むとx増加，左に進むとx減少）
- **Y軸**: 上が正の方向（上に進むとy増加，下に進むとy減少）
- **角度**: マットの上方向を基準に時計回りで測定

```
        Y軸
        ↑
        │
   180°│
   ----●----  →  X軸  →
        │ 0°
        ↓ 270°(または-90°)
```

### 角度の表現

キューブの向きは角度で表現される：

| 向き | 角度 | 説明 |
|------|------|------|
| マットの上方向 | 0° | デフォルト方向 |
| マットの右方向 | 90° | 時計回りに90° |
| マットの下方向 | 180°（または -180°） | 時計回りに180° |
| マットの左方向 | 270°（または -90°） | 反時計回りに90° |

**注意**: 角度は 0°〜359° で表現される（負の角度は対応していない）

### 実際の画像

*画像出典: https://github.com/toio/toio.py/blob/main/SIMPLE_API.ja.md*

![toio coordinate system](fig/toio_coordinate_system_1.png)
![toio coordinate system](fig/toio_coordinate_system_2.png)

まずは簡単な例で動作を確認しよう．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # 現在の位置情報を取得
    position = cube.get_current_position()

    if position is not None:
        x, y = position
        print("現在の位置: X =", x, "Y =", y)
    else:
        print("位置情報が取得できませんでした")
```

</details>

---

## 位置情報と角度情報のAPI

### 現在の座標を取得

```python
position = cube.get_current_position()  # (x, y)のタプルまたはNoneを返す
x = cube.get_x()  # x座標またはNoneを返す
y = cube.get_y()  # y座標またはNoneを返す
```

### 現在の角度を取得

```python
angle = cube.get_orientation()  # 角度（度）またはNoneを返す
```

**注意**: これらの関数はキューブがマット上にある場合のみ正しい値を返す．
マット上にない場合は `None` が返る．

### やってみよう 

**課題1（易）**: 現在のx座標とy座標を取得し，表示せよ．

**課題2（中）**: 現在の角度を取得し，「現在の向き: XX度」と表示せよ．

**課題3（難）**: 位置と角度を0.5秒ごとに継続的に表示するプログラムを書け（Ctrl+Cで終了）．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `while True:` でループ
- `position = cube.get_current_position()` で位置を取得
- `angle = cube.get_orientation()` で角度を取得
- `if position is not None:` でNoneチェック
- `x, y = position` でタプルをアンパック
- `cube.sleep(0.5)` でポーリング間隔を設定
- `try: ... except KeyboardInterrupt:` でCtrl+C終了を処理

</details>

---

## 位置と角度を継続的に表示

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube

target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("位置と角度を読み取ります（Ctrl+Cで終了）")

    try:
        running = True
        while running:
            # 現在の位置情報と角度情報を取得
            position = cube.get_current_position()
            angle = cube.get_orientation()

            if position is not None and angle is not None:
                x, y = position
                print(f"位置: X = {x}, Y = {y}, 角度: {angle}度")
            else:
                print("位置情報が取得できません")

            cube.sleep(0.5)  # 0.5秒待つ

    except KeyboardInterrupt:
        print("\n終了します")
```

このプログラムの動作：

1. 位置と角度を0.5秒ごとに継続的に取得
2. 位置情報と角度情報を表示
3. Ctrl+Cで終了

</details>
