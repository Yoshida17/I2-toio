---
layout: default
title: "センサー入力"
parent: "1日目"
nav_order: 50
---

# センサー入力

## センサー入力の基礎

toioキューブには様々なセンサーが搭載されている：

1. **ボタン** - 押されているかを検出
2. **姿勢センサー** - どの面が上かを検出
3. **傾きセンサー** - 3軸の傾き角度を検出

まずは簡単な例で動作を確認しよう．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # ボタンの状態を確認
    button_state = cube.is_button_pressed()

    if button_state == 128:
        print("ボタンが押されています")
    else:
        print("ボタンは押されていません")
```

</details>

---

## センサー入力のAPI

### ボタンの状態を取得

```python
button_state = cube.is_button_pressed()
```

**戻り値**:

- `0`: ボタンが押されていない
- `128`: ボタンが押されている
- `None`: 状態を正しく検出できない場合

### やってみよう 

**課題1（易）**: ボタンの状態を取得し，押されていたら「ON」，押されていなければ「OFF」と表示せよ．

**課題2（中）**: ボタンが押されたら緑色のLED，押されていなければ赤色のLEDを点灯させよ．

**課題3（難）**: ボタンを押していない間は音が鳴り続け，ボタンを押したらプログラムが終了するプログラムを書け．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `while True:` でループ
- `cube.is_button_pressed()` で毎回チェック
- `cube.play_sound(note, duration, wait_to_complete=False)` で音を鳴らす（ブロックしない）
- ボタンが押されたら `break` でループを抜ける
- `cube.sleep(0.1)` でポーリング間隔を設定

</details>

### 姿勢（どの面が上か）を取得

```python
posture = cube.get_posture()
```

**戻り値**:

- `1`: 上面が上（通常の置き方）
- `2`: 底面が上（ひっくり返っている）
- `3`, `4`, `5`, `6`: 各側面が上
- `None`: 検出できない場合

### やってみよう 

**課題1（易）**: 姿勢を取得し，戻り値をそのまま表示せよ．

**課題2（中）**: 通常の置き方（posture == 1）なら緑色LED，ひっくり返っている（posture == 2）なら赤色LEDを点灯させよ．

**課題3（難）**: 姿勢に応じて異なる音を鳴らすプログラムを書け（通常：高い音，ひっくり返し：低い音）．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `cube.get_posture()` で姿勢を取得
- `if posture == 1:` で通常の置き方をチェック
- `elif posture == 2:` でひっくり返しをチェック
- 高い音：`cube.play_sound(72, 0.5)`，低い音：`cube.play_sound(48, 0.5)`

</details>

### 傾き角度を取得

```python
angles = cube.get_3d_angle()
```

**戻り値**: `(roll, pitch, yaw)` のタプル，または `None`

- `roll`: 左右への傾き（X軸周りの回転）
- `pitch`: 前後への傾き（Y軸周りの回転）
- `yaw`: 水平面での回転（Z軸周りの回転）

各値は角度（度）で返される．

*画像出典: https://toio.io/*

![toioキューブの3軸](fig/sensor_cube_axis-c811d07901943cf1d221286bf5c2bff4.svg)

*図：toioキューブの3軸（roll, pitch, yaw）の定義*

### やってみよう 

**課題1（易）**: 傾き角度を取得し，roll, pitch, yawの3つの値を表示せよ．

**課題2（中）**: rollが10度以上なら「右に傾いている」，-10度以下なら「左に傾いている」と表示せよ．

**課題3（難）**: 前に傾けたら（pitch < -10）緑色LED，後ろに傾けたら（pitch > 10）赤色LEDを点灯させるプログラムを書け（Ctrl+Cで終了）．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `while True:` でループ
- `angles = cube.get_3d_angle()` で角度を取得
- `if angles is not None:` でNoneチェック
- `roll, pitch, yaw = angles` でタプルをアンパック
- `cube.sleep(0.3)` でポーリング間隔を設定

</details>

---

## プログラム例

### 例1：ボタンを押したらスタート

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube

target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("ボタンを押すと前進します（Ctrl+Cで終了）")

    try:
        running = True
        while running:
            button_state = cube.is_button_pressed()

            if button_state == 128:
                print("スタート！")
                cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑色に光る
                cube.play_sound(72, 0.3)  # スタート音（0.3秒ブロック）
                cube.move(60, 2)  # 2秒間前進
                cube.sleep(0.5)  # 前進後に少し待つ

            cube.sleep(0.1)  # 少し待ってから再度チェック

    except KeyboardInterrupt:
        print("\n終了します")
```

</details>

### 例2：姿勢に応じて動作を変える

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # 現在の姿勢を取得
    posture = cube.get_posture()

    if posture is not None:
        print(f"現在の姿勢: {posture}")

        if posture == 1:
            # 通常の置き方 - 前進
            print("通常の置き方です - 前進します")
            cube.turn_on_cube_lamp(0, 255, 0, 1)  # 緑
            cube.move(50, 2)
            cube.sleep(2)

        elif posture == 2:
            # ひっくり返っている - LEDと音で警告（モーターは動かさない）
            print("ひっくり返っています")
            cube.turn_on_cube_lamp(255, 0, 0, 1)  # 赤（1秒）
            cube.play_sound(48, 0.5)  # 警告音（0.5秒ブロック）
            cube.sleep(0.5)  # LED消灯まで待つ

        elif posture in [3, 4, 5, 6]:
            # 側面が上 - LEDと音で通知（モーターは動かさない）
            print("側面が上です")
            cube.turn_on_cube_lamp(0, 0, 255, 1)  # 青（1秒）
            cube.play_sound(60, 0.3)  # 通知音（0.3秒ブロック）
            cube.sleep(0.7)  # LED消灯まで待つ
    else:
        print("姿勢を検出できませんでした")
```

このプログラムの動作：

1. キューブの姿勢を取得
2. 通常の置き方なら前進（緑色）
3. ひっくり返っているなら警告音とLED（赤色）
4. 側面が上なら通知音とLED（青色）

</details>

### 例3: 傾きを検出する

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube

target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("キューブを傾けると反応します（Ctrl+Cで終了）")

    try:
        running = True
        while running:
            angles = cube.get_3d_angle()

            if angles is not None:
                roll, pitch, yaw = angles

                # ロール（左右の傾き）をチェック
                if roll > 10:  # 右に傾いている
                    cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤
                    print(f"右に傾いています（ロール: {roll}度）")

                elif roll < -10:  # 左に傾いている
                    cube.turn_on_cube_lamp(0, 0, 255, 0.5)  # 青
                    print(f"左に傾いています（ロール: {roll}度）")

                # ピッチ（前後の傾き）をチェック
                elif pitch < -10:  # 前に傾いている
                    cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑
                    print(f"前に傾いています（ピッチ: {pitch}度）")

                elif pitch > 10:  # 後ろに傾いている
                    cube.turn_on_cube_lamp(255, 255, 0, 0.5)  # 黄
                    print(f"後ろに傾いています（ピッチ: {pitch}度）")

                else:
                    cube.turn_off_cube_lamp()

            cube.sleep(0.3)  # 0.3秒ごとにチェック

    except KeyboardInterrupt:
        print("\n終了します")
```

このプログラムの動作：

1. 常にキューブの傾き角度を監視
2. 傾きが10度以上になると色とメッセージで知らせる
3. 右傾き：赤，左傾き：青，前傾き：緑，後ろ傾き：黄

</details>

### 例4: 傾きで方向を制御

このプログラムはtoioを固めで滑りにくい板の上に乗せて実行する．板を傾けるとその傾きに応じてtoioが移動する．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube

target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("キューブを傾けて方向を操作します（Ctrl+Cで終了）")
    print("前傾：前進，後傾：後退，左傾：左回転，右傾：右回転")

    # モーターを継続的に動かす
    cube.move(0, 0)  # 最初は停止状態

    try:
        running = True
        while running:
            angles = cube.get_3d_angle()

            if angles is not None:
                roll, pitch, yaw = angles

                # ロール（左右の傾き）で回転を制御
                if roll > 10:
                    cube.spin(20, 0)  # 左回転
                    print("左回転中")
                elif roll < -10:
                    cube.spin(-20, 0)  # 右回転
                    print("右回転中")

                # ピッチ（前後の傾き）で前進・後退を制御
                elif pitch < -5:
                    cube.move(20, 0)  # 前進
                    print("前進中")
                elif pitch > 5:
                    cube.move(-20, 0)  # 後退
                    print("後退中")

                else:
                    cube.stop_motor()  # 停止

            cube.sleep(0.1)

    except KeyboardInterrupt:
        print("\n終了します")
```

このプログラムの動作：

1. キューブの傾きを常に監視
2. 前に傾けると前進，後ろに傾けると後退
3. 左に傾けると左回転，右に傾けると右回転
4. 傾きが小さいときは停止

</details>

---

## センサー入力を使う際のポイント

1. **None チェック**: センサーの戻り値は `None` の可能性があるため，必ずチェックする．

2. **ポーリング間隔**: センサーを連続的に読み取る場合，適切な間隔（0.1〜0.5秒程度）で `cube.sleep()` を入れる．

3. **傾き検出の閾値**: 傾き角度で動作を変える場合，10度程度の閾値を設定すると誤動作を防げる．

4. **ボタンの長押し検出**: ボタンが押されている間は `128` が返り続けるため，長押しの検出も可能である．

5. **センサーと動作の組み合わせ**: センサー入力とモーター制御，LED，音を組み合わせると，インタラクティブなプログラムを作れる．

---

## 応用：Cubeクラスを使った衝突検知

**注意**: このセクションは発展的な内容である．より高度なプログラミングに興味がある人向けの内容となっている．

### SimpleCube APIの限界

これまで使ってきたSimpleCube APIでは，衝突検知機能を直接使うことができない．角度の変化で衝突を検知しようとしても，toioキューブは非常に安定しているため，壁にぶつかっても角度がほとんど変化しない（最大でも3度程度）．

### Cubeクラスとは

toio.pyには2つのAPI階層がある：

- **SimpleCube API**: 初心者向けの同期的なAPI（これまで使ってきたもの）
- **Cubeクラス（非同期API）**: より詳細な制御が可能な高度なAPI

Cubeクラスを使うと，SimpleCube APIでは使えない以下の機能が利用できる：

- モーション検出（衝突検知，ダブルタップ，揺れ検知）
- より詳細なセンサー情報
- 複数キューブの同時制御

### 非同期処理とは

Cubeクラスは**非同期処理（async/await）**を使う．これは，複数の処理を効率的に実行するためのPythonの仕組みである．

**基本的なパターン**：

```python
import asyncio

async def main():
    # async関数の中では await を使う
    await cube.connect()
    await cube.api.motor.motor_control(50, 50, 0)

# プログラムを実行
asyncio.run(main())
```

### 衝突検知のサンプルコード

```python
from toio import *
from toio.scanner import BLEScanner
import asyncio

# キューブ名を指定
target_cube_name = "toio-xxx"  # 実際のキューブ名に置き換え

# 衝突検知フラグ
collision_detected = False

async def main():
    global collision_detected

    # toioキューブをスキャンして接続
    print(f"{target_cube_name}を探しています...")
    devices = await BLEScanner.scan(3)

    # 指定されたキューブを探す
    target_device = None
    for device in devices:
        if device.name == target_cube_name:
            target_device = device
            break

    if target_device is None:
        print(f"{target_cube_name}が見つかりませんでした")
        return

    cube = ToioCoreCube(target_device.interface)
    await cube.connect()
    print("接続しました")

    # 衝突検知のハンドラ（ペイロードを直接解析）
    def motion_handler(payload: bytearray):
        global collision_detected
        # toio Core Cube仕様に従ってペイロードを解析
        # バイト位置2が衝突検知 (0x00: なし, 0x01: あり)
        if len(payload) > 2 and payload[2] == 0x01:
            print("衝突を検知しました！")
            collision_detected = True

    # 通知ハンドラーを登録
    await cube.api.sensor.register_notification_handler(motion_handler)

    # モーション情報をリクエスト（通知を有効化）
    await cube.api.sensor.request_motion_information()

    # スタート音とLED
    await cube.api.indicator.turn_on([1000, 0, 255, 0])  # [duration_ms, r, g, b]
    await cube.api.sound.play_sound_effect(2, 255)  # sound_id, volume
    await asyncio.sleep(1.0)

    # 前進開始
    print("前進します（何かにぶつかると停止します）")
    await cube.api.motor.motor_control(50, 50, 0)  # 左速度, 右速度, duration_ms

    # 衝突検知を待つ（最大10秒）
    for _ in range(100):
        if collision_detected:
            break
        await asyncio.sleep(0.1)

    # 停止
    await cube.api.motor.motor_control(0, 0, 0)

    if collision_detected:
        # 衝突検知時
        await cube.api.indicator.turn_on([1000, 255, 0, 0])
        await cube.api.sound.play_sound_effect(7, 255)
        await asyncio.sleep(1.0)

        # 少し後退
        await cube.api.motor.motor_control(-30, -30, 1000)
        await asyncio.sleep(1.5)
    else:
        print("時間切れです")
        await cube.api.indicator.turn_on([1000, 0, 255, 255])

    print("完了！")
    await cube.disconnect()

# プログラムを実行
asyncio.run(main())
```



### このプログラムの動作

1. toioキューブをスキャンして接続
2. 衝突検知の通知ハンドラーを登録
3. 緑色に光って音を鳴らす
4. 前進開始
5. 衝突を検知したら停止
6. 赤色に光って警告音を鳴らし，後退する

### さらに学びたい人へ

- **toio.py公式リポジトリ**: [https://github.com/toio/toio.py](https://github.com/toio/toio.py)
- **toio Core Cube技術仕様**: [https://toio.github.io/toio-spec/](https://toio.github.io/toio-spec/)
- **Pythonの非同期処理**: async/awaitの詳細を学ぶと，より複雑なプログラムが書けるようになる
