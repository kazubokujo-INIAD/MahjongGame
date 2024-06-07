import random
import time
import hashlib
import time
import tkinter as tk

# マージャンの牌の種類とその番号の対応
mahjong_tiles = {
    0: "一萬", 1: "二萬", 2: "三萬", 3: "四萬", 4: "五萬", 5: "六萬", 6: "七萬", 7: "八萬", 8: "九萬",
    9: "一筒", 10: "二筒", 11: "三筒", 12: "四筒", 13: "五筒", 14: "六筒", 15: "七筒", 16: "八筒", 17: "九筒",
    18: "一索", 19: "二索", 20: "三索", 21: "四索", 22: "五索", 23: "六索", 24: "七索", 25: "八索", 26: "九索",
    27: "東", 28: "南", 29: "西", 30: "北",
    31: "白", 32: "發", 33: "中"
}

#和了処理
def result(pai):
    return pai

# 乱数シード生成関数
def generate_seed():
    current_time = str(time.time()).encode('utf-8')
    hashed_time = hashlib.sha256(current_time).hexdigest()
    seed_value = int(hashed_time, 16)
    return seed_value

# 乱数シャッフル関数
def shuffle_list_with_random_seed(lst):
    seed_value = generate_seed()
    random.seed(seed_value)
    shuffled_list = lst[:]
    random.shuffle(shuffled_list)
    return shuffled_list

# 牌の配布関数
def distribute_tiles(original_list, player_list, cp2_list, cp3_list, cp4_list):
    all_lists = [player_list, cp2_list, cp3_list, cp4_list]

    for i, tile in enumerate(original_list):
        current_list = all_lists[i % 4]
        if len(current_list) < 13:
            current_list.append(tile)
            if current_list is player_list:  # playerの手札が配られる場合
                display_tiles_by_id(player_list)  # playerの牌を表示
                #time.sleep(1)  # 1秒遅延
                print()

    for lst in all_lists:
        lst.sort()

    return player_list, cp2_list, cp3_list, cp4_list

# 牌の表示関数
def display_tiles_by_id(tile_list):
    tiles = [mahjong_tiles.get(tile_id) for tile_id in tile_list]
    return " ".join(tiles)

# GUIで牌を表示する関数
def display_tiles_gui(tile_list):
    # Tkinterウィンドウの作成
    root = tk.Tk()
    root.title("Mahjong Tiles Display")  # ウィンドウのタイトル

    # 牌を表示するラベルを作成して配置
    tiles_text = display_tiles_by_id(tile_list)
    label = tk.Label(root, text=tiles_text, font=("Arial", 12), wraplength=300)
    label.pack()

    # Tkinterウィンドウの表示
    root.mainloop()

# プレイヤーの行動処理関数
def process_player_action(action):
    if action == "r":
        result(player)
        print("プレイヤーが和了りました！")

    elif action == "d":
        tile_to_discard = input("捨てる牌を選んでください: ")
        if tile_to_discard.isdigit():  # 入力が数字かどうかを確認
            tile_to_discard = int(tile_to_discard)
            if tile_to_discard in player:  # プレイヤーの手札に選択した牌があるか確認
                player.remove(tile_to_discard)  # 選択した牌を手札から削除
                print("牌を捨てました:", mahjong_tiles[tile_to_discard])
            else:
                print("手札にその牌はありません。")
        else:
            print("数字を入力してください。")

# プレイヤーの行動関数
def player_action():
    display_tiles_by_id(player)
    if pai_yama:  # 牌山に牌が残っている場合
        drawn_tile = pai_yama.pop(0)  # 牌山の先頭から牌をツモる
        player.append(drawn_tile)
        print("牌をツモりました:", mahjong_tiles[drawn_tile])

        action = input("行動を選択してください（捨てる: d, 和了る: r）: ")
        process_player_action(action)
    else:
        print("牌山に牌がありません。流局です。")
        restart_game = input("ゲームをリスタートしますか？ (y/n): ")
        if restart_game.lower() == "y":
            # ゲームをリスタートする処理を記述するか、必要なら進行する処理を記述する
            pass  # ゲームをリスタートする処理や進行する処理を追加する
        else:
            print("ゲームを終了します。")




# 他のプレイヤーの行動シミュレート関数
def simulate_other_players_actions(cp2, cp3, cp4):
    players = [cp2, cp3, cp4]
    players_name = {'cp2': cp2, 'cp3': cp3, 'cp4': cp4}
    for cp in players:
        player_name = next(name for name, player in players_name.items() if player == cp)
        if cp:  # 手札がある場合
            if pai_yama:  # 牌山に牌が残っている場合
                drawn_tile = pai_yama.pop(0)  # 牌山の先頭から牌をツモる
                cp.append(drawn_tile)
                #time.sleep(2)
                print()
                print(f"{player_name}が牌をツモりました")
                

                # 手札からランダムに1枚の牌を捨てる処理
                discarded_tile = random.choice(cp)
                cp.remove(discarded_tile)
                #time.sleep(2)
                print(f"{player_name}が牌を捨てました: {mahjong_tiles[discarded_tile]}")
            else:
                print("牌山に牌がありません。流局です。")
                restart_game = input("ゲームをリスタートしますか？ (y/n): ")
                if restart_game.lower() == "y":
                    # ゲームをリスタートする処理を記述するか、必要なら進行する処理を記述する
                    pass  # ゲームをリスタートする処理や進行する処理を追加する
                else:
                    print("ゲームを終了します。")
                    return  # ゲームを終了する場合は関数から抜ける
        else:
            print(f"{player_name}の手札がありません。")




# ゲーム終了条件判定関数
def game_end_condition():
    # TODO: ゲームの終了条件を判定する処理を実装する
    return False  # ゲームが終了していない場合はFalseを返す

# ゲームの進行関数
def game_progress():
    player_action_choice = player_action()
    process_player_action(player_action_choice)
    simulate_other_players_actions(cp2, cp3, cp4)
    if not game_end_condition():
        display_tiles_gui(player)  # プレイヤーの手牌をGUIで表示
        root.destroy()  # ゲーム終了時にウィンドウを閉じる
    else:
        root.after(1000, game_progress)  # 1000ミリ秒後に再度ゲームを進行する


# ゲームの進行関数
def game_progress(player):
    player_action_choice = player_action()
    process_player_action(player_action_choice)
    simulate_other_players_actions(cp2, cp3, cp4)
    if not game_end_condition():
        display_tiles_gui(player)  # プレイヤーの手牌をGUIで表示
        root.destroy()  # ゲーム終了時にウィンドウを閉じる
    else:
        root.after(1000, lambda: game_progress(player))  # 1000ミリ秒後に再度ゲームを進行する
# 牌の準備とゲームの進行
if __name__ == "__main__":
    pai = [i for i in range(34) for _ in range(4)]  # 牌のリスト（136枚）
    pai_yama = shuffle_list_with_random_seed(pai)

    # プレイヤーおよび他のプレイヤーの手札を配る
    player, cp2, cp3, cp4 = distribute_tiles(pai_yama, [], [], [], [])

    # Tkinterウィンドウを作成してゲームを進行
    root = tk.Tk()
    root.title("Mahjong Game")  # ウィンドウのタイトル
    display_tiles_gui(player)  # 初めにプレイヤーの手牌をGUIで表示

    root.after(2000, lambda: game_progress(player))  # 2000ミリ秒後にゲームを進行する
    root.mainloop()
