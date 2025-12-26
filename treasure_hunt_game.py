"""
toio宝探しゲーム用クラスモジュール

このモジュールは，コンテスト課題「宝探しゲーム」の主要なロジックを
TreasureHuntGameクラスとして提供する．
宝の配置，プレイヤーからの距離計算，宝の取得判定，ゲーム状態の管理などを行う．

使い方:
    from treasure_hunt_game import TreasureHuntGame
    from toio.simple import SimpleCube

    game = TreasureHuntGame()
    game.initialize_treasures(3)  # 宝を3個配置（自動でゲーム開始時刻を記録）

    with SimpleCube() as cube:
        # 距離レベルを取得
        distance = game.get_treasure_distance(cube)

        # 宝の取得を試みる
        success = game.try_collect_treasure(cube)
        # 全ての宝を取得した場合，自動でゲーム終了時刻を記録して表示
"""

import random
import time
from toio.simple import SimpleCube


class TreasureHuntGame:
    """
    toio宝探しゲームのロジックと状態を管理するクラス．

    宝の配置，プレイヤーのキューブからの距離計算，宝の取得判定，
    そしてゲームの状態（見つかった宝の数など）をカプセル化する．
    """

    # マットの座標範囲
    MAT_X_MIN = -135
    MAT_X_MAX = 135
    MAT_Y_MIN = -90
    MAT_Y_MAX = 90

    # 距離の閾値
    COLLECT_DISTANCE = 15  # 取得可能な距離
    DISTANCE_CLOSE = 60  # 近い
    DISTANCE_FAR = 100  # 遠い

    def __init__(self):
        """
        TreasureHuntGameクラスの新しいインスタンスを初期化する．
        ゲームの状態（宝の位置と取得状況）はここでリセットされる．
        """
        self.__treasures = []  # 配置された全ての宝の座標リスト（カプセル化）
        self.__collected_treasures = []  # 取得済みの宝の座標リスト（カプセル化）
        self.__start_time = None  # ゲーム開始時刻（カプセル化）
        self.__finish_time = None  # ゲーム終了時刻（カプセル化）
        print("TreasureHuntGameの準備ができました．")

    def initialize_treasures(self, num_treasures: int = 1) -> int:
        """
        宝をランダムな位置に配置し，ゲームを初期化する．
        このメソッドはゲーム開始時に1回だけ呼び出す必要がある．
        宝同士はマンハッタン距離で30以上離れるように配置される．

        ゲーム開始時刻は自動的に記録される．

        Args:
            num_treasures (int): 配置する宝の個数（デフォルト: 1）
                                推奨値: 1（初心者），3（標準），5（上級者）
                                最大値: 5

        Returns:
            int: 配置した宝の個数

        Example:
            >>> game = TreasureHuntGame()
            >>> game.initialize_treasures(3)  # 宝を3個配置（自動でゲーム開始時刻を記録）
            3
        """
        self.__treasures = []
        self.__collected_treasures = []
        min_manhattan_dist = 30  # 宝同士の最小マンハッタン距離

        # 少数の場合は四捨五入（0.5以上なら切り上げ）
        original_num = num_treasures
        num_treasures = int(num_treasures + 0.5)
        if num_treasures != original_num:
            print(f"注記：宝の個数を四捨五入しました（{original_num} → {num_treasures}個）")

        # 宝の個数が5を超える場合は調整
        if num_treasures > 5:
            print(f"警告：宝の個数は最大5個までです．{num_treasures}個から5個に修正しました．")
            num_treasures = 5

        print(f"\n{num_treasures}個の宝を配置しています...")

        while len(self.__treasures) < num_treasures:
            x = random.randint(self.MAT_X_MIN, self.MAT_X_MAX)
            y = random.randint(self.MAT_Y_MIN, self.MAT_Y_MAX)
            new_treasure = (x, y)

            # 他の宝との距離が十分かチェック
            is_far_enough = True
            if self.__treasures:  # 既に宝が1つ以上ある場合
                for existing_treasure in self.__treasures:
                    manhattan_dist = abs(x - existing_treasure[0]) + abs(y - existing_treasure[1])
                    if manhattan_dist < min_manhattan_dist:
                        is_far_enough = False
                        break  # 条件を満たさないので，この候補は破棄

            if is_far_enough:
                self.__treasures.append(new_treasure)

        print(f"\n{num_treasures}個の宝が隠されました！")
        print("toioを操作して宝を探そう．")
        print("宝の近くでtry_collect_treasureメソッドを実行すると取得できる．\n")

        # ゲーム開始時刻を自動的に記録
        self.__start_time = time.time()
        print("ゲームを開始しました．\n")

        return num_treasures

    def get_treasure_distance(self, cube: SimpleCube) -> float | None:
        """
        キューブの現在位置から，最も近い未取得の宝までの距離を返す．

        Args:
            cube (SimpleCube): toioキューブのSimpleCubeオブジェクト．
                               このオブジェクトから現在位置情報を取得する．

        Returns:
            float: 最も近い宝までの距離（ユニット）
            None: キューブの位置情報が取得できない場合，または全ての宝を取得済みの場合．

        Example:
            >>> distance = game.get_treasure_distance(cube)
            >>> if distance is not None:
            >>>     if distance <= 15:
            >>>         cube.turn_on_cube_lamp(255, 0, 0, 0.5)  # 赤色（とても近い）
            >>>     elif distance < 60:
            >>>         cube.turn_on_cube_lamp(255, 128, 0, 0.5)  # オレンジ（近い）
        """
        position = cube.get_current_position()
        if position is None:
            return None

        current_x, current_y = position

        remaining_treasures = [t for t in self.__treasures if t not in self.__collected_treasures]

        if not remaining_treasures:  # 全ての宝を取得済み
            return None

        min_distance = float('inf')
        for treasure_x, treasure_y in remaining_treasures:
            distance = ((current_x - treasure_x)**2 + (current_y - treasure_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance

        return min_distance

    def try_collect_treasure(self, cube: SimpleCube) -> bool | None:
        """
        キューブの現在位置で宝の取得を試みる．
        キューブが未取得の宝から `COLLECT_DISTANCE` ユニット以内にいる場合，宝を取得できる．
        取得成功時は，その宝が「取得済み」となり，次回から距離計算の対象外になる．

        全ての宝を取得した場合，自動的にゲーム終了時刻を記録し，所要時間を表示する．

        Args:
            cube (SimpleCube): toioキューブのSimpleCubeオブジェクト．

        Returns:
            bool: True - 宝を取得できた．
                  False - 宝が近くにない（取得失敗）．
            None: キューブの位置情報が取得できない場合．

        Example:
            >>> success = game.try_collect_treasure(cube)
            >>> if success:
            >>>     print("宝を発見！")
            >>>     cube.play_sound(72, 0.5)  # 成功音
            >>> else:
            >>>     print("宝はここにありません...")
        """
        position = cube.get_current_position()
        if position is None:
            return None

        current_x, current_y = position

        remaining_treasures = [t for t in self.__treasures if t not in self.__collected_treasures]

        for treasure_x, treasure_y in remaining_treasures:
            distance = ((current_x - treasure_x)**2 + (current_y - treasure_y)**2)**0.5

            if distance <= self.COLLECT_DISTANCE:
                self.__collected_treasures.append((treasure_x, treasure_y))
                collected_count = len(self.__collected_treasures)
                total_count = len(self.__treasures)
                print(f"\n★ 宝を発見しました！ ({collected_count}/{total_count}) ★")

                if collected_count == total_count:
                    print("\nおめでとうございます！全ての宝を発見しました！\n")
                    # 全ての宝を取得したため，自動的にゲーム終了を処理
                    self._finish_game_internal()

                return True

        return False

    def get_remaining_treasures(self) -> int:
        """
        残りの宝の個数を返す．

        Returns:
            int: まだ取得されていない宝の個数．

        Example:
            >>> remaining = game.get_remaining_treasures()
            >>> print(f"残り {remaining} 個の宝があります")
        """
        return len(self.__treasures) - len(self.__collected_treasures)

    def _finish_game_internal(self):
        """
        内部メソッド：ゲーム終了時刻を記録し，所要時間と取得した宝の数を表示する．
        try_collect_treasure()で全ての宝を取得した時に自動的に呼ばれる．
        """
        self.__finish_time = time.time()

        if self.__start_time is not None:
            elapsed_seconds = int(self.__finish_time - self.__start_time)
            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60
            collected_count = len(self.__collected_treasures)
            total_count = len(self.__treasures)

            print(f"\n========================================")
            print(f"ゲーム終了！")
            print(f"取得した宝: {collected_count}/{total_count}個")
            print(f"所要時間: {minutes}分{seconds:02d}秒")
            print(f"========================================\n")
        else:
            print("ゲーム開始時刻が記録されていません．")

    def finish_game(self):
        """
        ゲーム終了時刻を記録し，所要時間と取得した宝の数をm分ss秒の形式で表示する．

        通常は自動的に呼ばれるため，このメソッドは手動で呼び出す必要はない．
        手動でゲーム終了を処理したい場合のみ使用する．

        Example:
            >>> game.finish_game()  # 手動でゲーム終了を処理
        """
        self._finish_game_internal()

    def reset_game(self):
        """
        ゲームの状態（宝の位置と取得状況）をリセットする．
        新しいゲームを始める前に，またはゲームをやり直す際に呼び出す．

        Example:
            >>> game.reset_game()
            >>> game.initialize_treasures(5)  # 新しいゲームを開始
        """
        self.__treasures = []
        self.__collected_treasures = []
        self.__start_time = None
        self.__finish_time = None
        print("ゲームをリセットしました．")
