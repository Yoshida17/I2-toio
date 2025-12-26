---
layout: default
title: "キーボード操作"
parent: "2日目"
nav_order: 13
---

# キーボード操作

toioキューブをキーボードで操作することで，リアルタイムに動きをコントロールできる．
ここでは，操作感が全く異なる**2つのパターン**を紹介する．

## キーボード入力の仕組み（pynputライブラリ）

Pythonでキーボード入力をリアルタイムに取得するには，`pynput`ライブラリを使う．

**基本的な使い方**：

<details markdown="1">
<summary>プログラム例を見る</summary>

矢印↑キーを押すと画面にprintする．qキーでプログラム終了．

```python
from pynput import keyboard
from pynput.keyboard import KeyCode

# 現在押されているキーを追跡
current_keys = set()
should_exit = False

def on_press(key):
    """キーが押された時に呼ばれる"""
    global should_exit
    if key == KeyCode.from_char('q'):
        should_exit = True
    current_keys.add(key)

def on_release(key):
    """キーが離された時に呼ばれる"""
    current_keys.discard(key)

# リスナーを開始（suppress=Trueで他アプリに渡さない）
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True
)
listener.start()

# メインループ
while not should_exit:
    if keyboard.Key.up in current_keys:
        print("上キーが押されている")
    # ...

listener.stop()
```

</details>

### キーの種類と判定方法

pynputライブラリでは，キーを2種類に分けて扱う．

**1. 特殊キー**（矢印キー，スペースキーなど）

`keyboard.Key.キー名`の定数で判定する．

```python
if keyboard.Key.up in current_keys:
    # 上矢印キーが押されている
```

**よく使う特殊キーの定数**：

| キー    | 定数                   |
| ----- | -------------------- |
| 上矢印   | `keyboard.Key.up`    |
| 下矢印   | `keyboard.Key.down`  |
| 左矢印   | `keyboard.Key.left`  |
| 右矢印   | `keyboard.Key.right` |
| スペース  | `keyboard.Key.space` |
| Enter | `keyboard.Key.enter` |
| Esc   | `keyboard.Key.esc`   |
| Shift | `keyboard.Key.shift` |
| Ctrl  | `keyboard.Key.ctrl`  |
| Alt   | `keyboard.Key.alt`   |

**2. 文字キー**（アルファベット，数字）

`KeyCode.from_char()`を使って判定する．

```python
from pynput.keyboard import KeyCode

# 特殊キーと同じようにシンプルに判定できる
if KeyCode.from_char('w') in current_keys:
    # wキーが押されている
```

**WASDキーで操作する例**：

```python
from pynput.keyboard import KeyCode

# メインループ
while not should_exit:
    if KeyCode.from_char('w') in current_keys:
        cube.move(30, 0)  # 前進
    elif KeyCode.from_char('s') in current_keys:
        cube.move(-30, 0)  # 後退
    elif KeyCode.from_char('a') in current_keys:
        cube.spin(-30, 0)  # 左回転
    elif KeyCode.from_char('d') in current_keys:
        cube.spin(30, 0)  # 右回転
    else:
        cube.stop_motor()
```

---

## パターン1: 直接操作

**特徴**: 矢印キーを押している間，連続的に動く

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
from pynput import keyboard
from pynput.keyboard import KeyCode

# 現在押されているキーを追跡
current_keys = set()
should_exit = False

def on_press(key):
    global should_exit
    if key == KeyCode.from_char('q'):
        should_exit = True
    current_keys.add(key)

def on_release(key):
    current_keys.discard(key)

target_cube_name = "toio-xxx"

# リスナーを開始（suppress=Trueで他アプリに渡さない）
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True
)
listener.start()

with SimpleCube(name=target_cube_name) as cube:
    while not should_exit:
        moved = False

        if keyboard.Key.up in current_keys:
            cube.move(30, 0)  # 前進
            moved = True
        elif keyboard.Key.down in current_keys:
            cube.move(-30, 0)  # 後退
            moved = True
        elif keyboard.Key.left in current_keys:
            cube.spin(-30, 0)  # 左回転
            moved = True
        elif keyboard.Key.right in current_keys:
            cube.spin(30, 0)  # 右回転
            moved = True

        if keyboard.Key.space in current_keys:
            cube.play_sound(60, 0.5)
            current_keys.discard(keyboard.Key.space)

        if not moved:
            cube.stop_motor()  # 停止

        cube.sleep(0.01)  # CPU負荷を減らす

listener.stop()
```

</details>

### 仕組みの詳細

**1. pynputリスナーの開始**

```python
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True  # 他アプリに渡さない
)
listener.start()
```

- `on_press`：キーが押された時に呼ばれる関数
- `on_release`：キーが離された時に呼ばれる関数
- `suppress=True`：矢印キーやスペースキーを他のアプリ（Thonnyなど）に渡さない
- バックグラウンドで動作し，キーの状態を常に監視

**2. キー状態の追跡**

```python
def on_press(key):
    current_keys.add(key)  # 押されたキーをセットに追加

def on_release(key):
    current_keys.discard(key)  # 離されたキーをセットから削除
```

- `current_keys`セットで現在押されているキーを管理
- キーが押されている間は`current_keys`に含まれる
- キーを離すと`current_keys`から削除される

**3. キー状態のチェック**

```python
if keyboard.Key.up in current_keys:
    # 上キーが押されている
```

- `keyboard.Key.up`などの定数でキーを判定
- `in current_keys`で現在押されているか確認
- リアルタイムなキー状態検出が可能

**4. 連続的な動作制御**

```python
cube.move(30, 0)  # duration=0 は「無制限」を意味する
```

- `duration=0`を指定することで，モーターが継続的に回転する
- キーが押されている間は常に前進し続ける
- キーを離すと`current_keys`から削除され，次のループで停止

**5. 停止制御**

```python
if not moved:
    cube.stop_motor()
```

- どのキーも押されていない場合，即座にモーターを停止
- これにより，キーを離した瞬間に止まる

**長所**：

- 直感的な操作感（押している間だけ動く）
- マット不要，どこでも動く
- 微調整が簡単（キーを軽く押せば少しだけ動く）

**短所**：

- 正確な距離や角度の制御は難しい
- キーを押し続ける必要がある

---

### やってみよう

**課題1（易）**: プログラム例を実行し，矢印キーでキューブを操作してみよ．qキーで終了することを確認せよ．

**課題2（中）**: スペースキーを押したときにLEDを赤く光らせるように変更せよ（音は鳴らさない）．

<details markdown="1">
<summary>ヒント（課題2）</summary>

スペースキーの処理部分を`cube.turn_on_cube_lamp(255, 0, 0, 0.5)`に変更する．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
# スペースキーの処理部分を変更
if keyboard.Key.space in current_keys:
    cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤く光る
    current_keys.discard(keyboard.Key.space)
```

</details>

**課題3（難）**: 前進・後退・回転の速度を50に変更せよ．また，スペースキーで音を鳴らし，同時に緑色に光るように変更せよ．

<details markdown="1">
<summary>ヒント（課題3）</summary>

`cube.move(速度, 0)`と`cube.spin(速度, 0)`の速度を変更．スペースキーの処理で`cube.play_sound()`と`cube.turn_on_cube_lamp()`の両方を呼ぶ．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
# 速度を50に変更
if keyboard.Key.up in current_keys:
    cube.move(50, 0)
    moved = True
elif keyboard.Key.down in current_keys:
    cube.move(-50, 0)
    moved = True
elif keyboard.Key.left in current_keys:
    cube.spin(-50, 0)
    moved = True
elif keyboard.Key.right in current_keys:
    cube.spin(50, 0)
    moved = True

# スペースキーで音と光
if keyboard.Key.space in current_keys:
    cube.turn_on_cube_lamp(0, 255, 0, 0)  # 緑
    cube.play_sound(60, 0.5)
    cube.turn_off_cube_lamp()             # LED消灯
    current_keys.discard(keyboard.Key.space)
```

</details>

---

## パターン2: 角度制御による滑らかな移動

**特徴**: 矢印キーを押している間，目標角度に向かって滑らかに移動する（マット必須）

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
from pynput import keyboard
from pynput.keyboard import KeyCode

# 現在押されているキーを追跡
current_keys = set()
should_exit = False

def normalize_angle(angle):
    """角度を-180～180の範囲に正規化"""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def on_press(key):
    global should_exit
    if key == KeyCode.from_char('q'):
        should_exit = True
    current_keys.add(key)

def on_release(key):
    current_keys.discard(key)

target_cube_name = "toio-xxx"

# リスナーを開始（suppress=Trueで他アプリに渡さない）
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True
)
listener.start()

with SimpleCube(name=target_cube_name) as cube:
    while not should_exit:
        current_angle = cube.get_orientation()

        if current_angle is None:
            cube.stop_motor()
            cube.sleep(0.1)
            continue

        target_angle = None

        if keyboard.Key.up in current_keys:
            target_angle = 0
        elif keyboard.Key.right in current_keys:
            target_angle = 90
        elif keyboard.Key.down in current_keys:
            target_angle = 180
        elif keyboard.Key.left in current_keys:
            target_angle = -90

        if target_angle is not None:
            angle_diff = normalize_angle(target_angle - current_angle)
            base_speed = 20
            turn_gain = 0.25
            left_speed = base_speed + turn_gain * angle_diff
            right_speed = base_speed - turn_gain * angle_diff
            left_speed = max(-100, min(100, int(left_speed)))
            right_speed = max(-100, min(100, int(right_speed)))
            cube.run_motor(left_speed, right_speed, 0)
        else:
            cube.stop_motor()

        cube.sleep(0.01)

listener.stop()
```

</details>

### 仕組みの詳細

**1. 角度差の計算**

```python
angle_diff = normalize_angle(target_angle - current_angle)
```

- 目標角度と現在の角度の差を計算
- `normalize_angle()`で-180～180度の範囲に正規化
  - 例：350度 → -10度（右に10度回転する方が近い）
  - 例：-170度 → -170度（そのまま）

**2. 左右モーター速度の計算**

```python
left_speed = base_speed + turn_gain * angle_diff
right_speed = base_speed - turn_gain * angle_diff
```

**計算例**：

- **正面を向いている（angle_diff = 0）**
  
  - `left_speed = 20 + 0.25 × 0 = 20`
  - `right_speed = 20 - 0.25 × 0 = 20`
  - → 左右同じ速度で直進

- **右に90度ずれている（angle_diff = 90）**
  
  - `left_speed = 20 + 0.25 × 90 = 42.5`
  - `right_speed = 20 - 0.25 × 90 = -2.5`
  - → 左モーターが速く，右モーターがほぼ停止して右旋回

- **左に45度ずれている（angle_diff = -45）**
  
  - `left_speed = 20 + 0.25 × (-45) = 8.75`
  - `right_speed = 20 - 0.25 × (-45) = 31.25`
  - → 右モーターが速く，左旋回しながら前進

**3. パラメータの意味**

- **base_speed（基本速度）**: 前進時の基本速度
  
  - 大きい → 速く移動するが制御が粗くなる
  - 小さい → ゆっくり移動するが精密に制御できる

- **turn_gain（旋回ゲイン）**: 角度差に対する旋回の強さ
  
  - 大きい → 素早く向きを変えるが，振動的になりやすい
  - 小さい → ゆっくり向きを変えるが，滑らかに移動

**4. run_motorによる個別モーター制御**

```python
cube.run_motor(left_speed, right_speed, 0)
```

- 左右のモーター速度を個別に指定
- これにより，前進しながら旋回する動作が可能
- `duration=0`で継続的に動作

**長所**：

- 目標方向に滑らかに向かう
- 前進しながら方向調整するため効率的
- パラメータ調整で動作特性を変更できる

**短所**：

- マットが必須（角度情報が必要）
- プログラムがやや複雑
- パラメータ調整が必要

---

### やってみよう

**課題1（易）**: プログラム例を実行し，矢印キーでキューブを操作してみよ．パターン1との違いを観察せよ．

**課題2（中）**: `base_speed`を60に変更して実行せよ．動きがどう変わるか観察せよ．

<details markdown="1">
<summary>ヒント（課題2）</summary>

プログラム内の`base_speed = 20`を`base_speed = 60`に変更する．

</details>

<details markdown="1">
<summary>解答例（課題2）</summary>

```python
# パラメータを変更
base_speed = 60  # 20から60に変更
turn_gain = 0.25
```

動きが速くなるが，方向転換がやや粗くなる．

</details>

**課題3（難）**: `turn_gain`を0.5に変更して実行せよ．動きがどう変わるか観察せよ．また，`base_speed`と`turn_gain`の両方を調整して，最も滑らかな動きになる値を見つけよ．

<details markdown="1">
<summary>ヒント（課題3）</summary>

`turn_gain = 0.25`を`turn_gain = 0.5`に変更．いくつかの値を試して比較する．

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
# turn_gainを0.5に変更
base_speed = 20
turn_gain = 0.5  # 0.25から0.5に変更
```

素早く向きを変えるが，振動的になりやすい．

</details>

---

## 2つのパターンの使い分け

| 項目            | パターン1（直接操作）        | パターン2（角度制御）     |
| ------------- | ------------------ | --------------- |
| **操作感**       | 押している間動く           | 押している間，目標角度に向かう |
| **必要な環境**     | マット不要              | マット必須           |
| **動き方**       | 直進・回転のみ            | 前進しながら旋回        |
| **制御方法**      | `move()`, `spin()` | `run_motor()`   |
| **向いている用途**   | 自由な探索，微調整          | 正確な方向移動，スムーズな制御 |
| **プログラムの難易度** | 簡単                 | やや複雑（角度計算あり）    |

**実際の応用例**：

- **宝探しゲーム（コンテスト課題）**: 両方とも使える
  - パターン1：シンプルで直感的
  - パターン2：滑らかな動きで探索
- **迷路ゲーム**: パターン2が向いている
  - 上下左右に正確に向きを変えられる
  - スムーズな動きで壁にぶつかりにくい

---

## 総合チャレンジ

### チャレンジ1: LED色で速度表示

パターン1のプログラムを改造し，前進時は緑，後退時は赤，回転時は青のLEDを光らせるプログラムを書け．

<details markdown="1">
<summary>ヒント</summary>

各キー判定の中で`cube.turn_on_cube_lamp(r, g, b, 0)`を呼ぶ．`duration=0`で継続的に光る．

</details>

<details markdown="1">
<summary>解答例</summary>

```python
# メインループ内の処理を変更
if keyboard.Key.up in current_keys:
    cube.move(30, 0)
    cube.turn_on_cube_lamp(0, 255, 0, 0)  # 緑
    moved = True
elif keyboard.Key.down in current_keys:
    cube.move(-30, 0)
    cube.turn_on_cube_lamp(255, 0, 0, 0)  # 赤
    moved = True
elif keyboard.Key.left in current_keys:
    cube.spin(-30, 0)
    cube.turn_on_cube_lamp(0, 0, 255, 0)  # 青
    moved = True
elif keyboard.Key.right in current_keys:
    cube.spin(30, 0)
    cube.turn_on_cube_lamp(0, 0, 255, 0)  # 青
    moved = True

if not moved:
    cube.stop_motor()
    cube.turn_off_cube_lamp()  # LEDを消す
```

</details>

### チャレンジ2: 角度制御に音を追加

パターン2のプログラムを改造し，角度差が大きいとき（30度以上）に警告音を鳴らすプログラムを書け．

<details markdown="1">
<summary>ヒント</summary>

`angle_diff`の絶対値をチェックし，30以上なら`cube.play_sound(音程, 0.1, wait_to_complete=False)`で音を鳴らす．

</details>

<details markdown="1">
<summary>解答例</summary>

```python
# 角度制御部分に追加
if target_angle is not None:
    angle_diff = normalize_angle(target_angle - current_angle)

    # 角度差が大きい場合に警告音
    if abs(angle_diff) > 30:
        cube.play_sound(50, 0.1, wait_to_complete=False)

    base_speed = 20
    turn_gain = 0.25
    left_speed = base_speed + turn_gain * angle_diff
    right_speed = base_speed - turn_gain * angle_diff
    left_speed = max(-100, min(100, int(left_speed)))
    right_speed = max(-100, min(100, int(right_speed)))
    cube.run_motor(left_speed, right_speed, 0)
else:
    cube.stop_motor()
```

</details>

---

## プログラム終了の仕組み（重要）

両方のパターンとも，**qキー**でプログラムを終了する．

```python
from pynput.keyboard import KeyCode

should_exit = False

def on_press(key):
    global should_exit
    if key == KeyCode.from_char('q'):
        should_exit = True
    current_keys.add(key)

# メインループ
with SimpleCube(name=target_cube_name) as cube:
    while not should_exit:
        # キーボード操作の処理
        ...

listener.stop()
```

**仕組み**：

1. `should_exit`フラグで終了を制御
2. qキーを押すと，`on_press()`関数内で`should_exit = True`になる
3. `while not should_exit`の条件が偽になり，ループを抜ける
4. `with SimpleCube(...)`を使っているため，自動的にtoioとの接続が切断される
5. `listener.stop()`でキーボードリスナーを停止

**pynputリスナーの管理**：

```python
listener = keyboard.Listener(...)
listener.start()  # リスナー開始
# ...
listener.stop()   # リスナー停止（終了時）
```

- リスナーはバックグラウンドで動作し続ける
- プログラム終了時に`stop()`でリスナーを停止
- これにより，キーイベントの監視を終了

**なぜこの仕組みが必要？**

- 無限ループ（`while not should_exit`）を使わないと，キーボード操作を繰り返せない
- 無限ループを安全に止めるには，終了条件（qキー）が必要
- `with`文のおかげで，toio接続が適切にクリーンアップされる
- `listener.stop()`でキーボード監視も適切に終了
