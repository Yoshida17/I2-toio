---
layout: default
title: "音とサウンド制御"
parent: "1日目"
nav_order: 40
---

# 音とサウンド制御

## 音制御の基礎

toioキューブは音を鳴らすことができる．音でプログラムの状態を伝えたり，メロディを演奏したりできる．

まずは簡単な例で動作を確認しよう．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    cube.play_sound(60, 1.0)  # ド（C4）の音を1秒間鳴らす
```

</details>

---

## 音制御のAPI

### 音を鳴らす

```python
cube.play_sound(note, duration)
```

パラメータ：

- `note`: 音階（0〜127のMIDI音階番号）
- `duration`: 再生時間（秒）．0.01〜2.55秒の範囲

**戻り値**: 成功した場合は `True`，失敗した場合は `False`

### やってみよう 

**課題1（易）**: 中央のド（60）の音を0.5秒，1秒，2秒と長さを変えて鳴らし，違いを確認せよ．

**課題2（中）**: MIDI番号を60, 65, 70, 75と変えて，音の高さの変化を確認せよ．

**課題3（難）**: 以下の動きをするプログラムを**自分で**書け：

- 低い音（48）を鳴らす → 1秒待つ → 高い音（72）を鳴らす

<details markdown="1">
<summary>ヒント（課題3）</summary>

- `cube.play_sound(note, duration)` を2回使う
- 音の間に無音時間が必要なら `cube.sleep()` で待機する

</details>

<details markdown="1">
<summary>解答例（課題3）</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx"
with SimpleCube(name=target_cube_name) as cube:
    cube.play_sound(48, 0.5)  # 低い音を0.5秒鳴らす
    cube.sleep(1)             # 1秒待つ
    cube.play_sound(72, 0.5)  # 高い音を0.5秒鳴らす
```

</details>

### 発展：ブロックしない音の再生

**デフォルトの動作**：`play_sound()`は音が鳴り終わるまでプログラムを停止する（ブロッキング動作）．

しかし，第3引数に`False`を指定すると，音を鳴らした後すぐに次の処理に進むことができる．

```python
# ブロックする（デフォルト）
cube.play_sound(60, 1.0)  # 1秒間停止
# ここに到達するのは1秒後

# ブロックしない
cube.play_sound(60, 1.0, False)  # すぐに次へ
# ここにすぐ到達
```

**使い分け**：

- 音が終わるまで待ちたい → `wait_to_complete=True`（デフォルト）
- 音を鳴らしながら他の処理をしたい → `wait_to_complete=False`

**例：音とLEDを同時に使う**

```python
# パターン1：順番に実行（ブロックする）
cube.play_sound(60, 1.0)  # 音を1秒鳴らす（1秒停止）
cube.turn_on_cube_lamp(255, 0, 0, 1.0)  # その後LEDを光らせる
# 合計2秒かかる

# パターン2：同時に実行（ブロックしない）
cube.play_sound(60, 1.0, False)  # 音を開始（すぐ次へ）
cube.turn_on_cube_lamp(255, 0, 0, 1.0)  # すぐLEDを光らせる
# 合計1秒で終わる（音とLEDが同時）
```

パターン2では，音とLEDが同時に開始されるため，より一体感のある演出ができる．

---

### 音を停止する

```python
cube.stop_sound()
```

現在再生中の音を即座に停止する．

---

## MIDI音階について

toioで使用する音階は，MIDI音階番号で指定する．

### よく使う音階の例

| 音名     | MIDI番号 | 説明        |
| ------ | ------ | --------- |
| C4（ド）  | 60     | 中央のド      |
| D4（レ）  | 62     |           |
| E4（ミ）  | 64     |           |
| F4（ファ） | 65     |           |
| G4（ソ）  | 67     |           |
| A4（ラ）  | 69     |           |
| B4（シ）  | 71     |           |
| C5（ド）  | 72     | 1オクターブ上のド |

**ポイント**:

- 半音上がるごとに番号が1増える
- 1オクターブ上がると番号が12増える
- C4（60）が基準の音（中央のド）

---

## 簡単なメロディを鳴らす

リストとforループを使って，複数の音を順番に鳴らすことができる．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("ドレミファソラシドを演奏します")

    # ドレミファソラシド のメロディ
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4からC5まで

    for note in notes:
        cube.play_sound(note, 0.5)  # 各音を0.5秒鳴らす
        cube.sleep(0.1)  # 少し間を空けて次の音へ（合計0.6秒間隔）

    print("演奏が完了しました")
```

</details>

### やってみよう 

**課題1（易）**: 上記のプログラムで，音の長さ（duration）を0.3秒に変えて，速いメロディにせよ．

**課題2（中）**: ドレミファソラシドを**逆順**（ドシラソファミレド）で演奏するプログラムを書け．

<details markdown="1">
<summary>ヒント（課題2）</summary>

- リストを逆順にするには `notes.reverse()` を使う
- または `reversed(notes)` を使う

</details>

**課題3（難）**: 好きなメロディ（4〜8音）を**自分で**作って演奏せよ．

<details markdown="1">
<summary>ヒント（課題3）</summary>

- MIDI音階表を参考に，好きな音階番号のリストを作る
- 音の長さを変えると，リズムが生まれる
- 例：`cube.play_sound(60, 0.5)` と `cube.play_sound(64, 0.3)` を交互に

</details>

---

## 動作と組み合わせた例

音とモーター制御を組み合わせることで，より豊かな表現ができる．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    print("前進しながら音階を上げます")

    # 前進しながら上昇音を鳴らす
    cube.move(20, 0)  # 前進開始（duration=0で継続）

    for note in range(60, 73):  # C4（60）からC5（72）まで
        cube.play_sound(note, 0.2)
        cube.sleep(0.05)  # 少し間を空ける（合計0.25秒間隔）

    cube.stop_motor()  # モーター停止

    print("ゴール音を鳴らします")
    # ゴール音（高い音を3回）
    for _ in range(3):
        cube.play_sound(84, 0.3)  # C6の音
        cube.sleep(0.1)  # 少し間を空ける（合計0.4秒間隔）

    print("演奏と動作が完了しました")
```

</details>

---

## 状況に応じた音の使い方

### ゴール音（成功音）

```python
# 明るい高い音を連続で鳴らす
cube.play_sound(72, 0.3)  # C5
cube.sleep(0.05)
cube.play_sound(76, 0.3)  # E5
cube.sleep(0.05)
cube.play_sound(79, 0.5)  # G5
```

### 警告音（エラー音）

```python
# 低い音を短く繰り返す
for _ in range(3):
    cube.play_sound(48, 0.2)  # C3（低い音）
    cube.sleep(0.1)  # 少し間を空ける
```

### スタート音（開始の合図）

```python
# 低い音から高い音へ素早く
cube.play_sound(55, 0.15)  # G3
cube.sleep(0.05)
cube.play_sound(67, 0.3)   # G4
```

---

## 音とLEDを組み合わせる

音とLEDを同時に使うことで，視覚と聴覚の両方で状態を伝えられる．

<details markdown="1">
<summary>プログラム例を見る</summary>

```python
from toio.simple import SimpleCube
target_cube_name = "toio-xxx" #実際のキューブ名に変更
with SimpleCube(name=target_cube_name) as cube:
    # 音とLEDで「準備完了」を表現

    print("カウントダウン開始")
    # カウントダウン音（3, 2, 1）
    for i in range(3):
        cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤く光る
        cube.play_sound(60, 0.5)  # 低めの音

    print("スタート！")
    # スタート！
    cube.turn_on_cube_lamp(0, 255, 0, 0.5)  # 緑に光る
    cube.play_sound(72, 0.5)  # 高い音

    print("前進します")
    # 前進開始
    cube.move(50, 2)

    print("動作が完了しました")
```

</details>

---

## 音を使う際のポイント

- **play_sound()はデフォルトでブロッキング動作**: `cube.play_sound(note, duration)` は指定した`duration`秒間プログラムを停止する．音が鳴り終わるまで次の処理には進まない．音を鳴らしながら他の処理をしたい 場合は第3引数に`False`を追加する．

---

## 総合チャレンジ

ここまで学んだ音制御APIを組み合わせて，以下の課題に挑戦しよう．

### チャレンジ1：警告音システム

以下の動作をするプログラムを書け：

1. 低い音（48）を0.2秒間，3回繰り返す（警告音）
2. 1秒待つ
3. 高い音（72）を0.5秒間鳴らす（確認音）

<details markdown="1">
<summary>ヒント</summary>

- `for _ in range(3):` で3回繰り返す
- 各音の後に短い `cube.sleep()` を入れる

</details>

### チャレンジ2：音楽プレイヤー

「きらきら星」の最初の音（ドドソソララソ）を演奏するプログラムを**自分で**書け．

<details markdown="1">
<summary>ヒント</summary>

- ド=60, ソ=67, ラ=69
- リスト: `[60, 60, 67, 67, 69, 69, 67]`
- forループで順番に再生

</details>

### チャレンジ3：音と動きの融合

以下の動作をするプログラムを作れ：

- 前進しながら上昇音（60→72）
- 停止して高い音（84）を3回
- 後退しながら下降音（72→60）

<details markdown="1">
<summary>ヒント</summary>

- `cube.move(speed, 0)` で継続的に移動
- `range(60, 73)` で上昇，`range(72, 59, -1)` で下降
- `cube.stop_motor()` で停止

</details>
