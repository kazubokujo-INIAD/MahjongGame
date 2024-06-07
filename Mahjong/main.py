import random
import time
import tkinter as tk
import hashlib

# マージャンの牌の種類とその番号の対応
mahjong_tiles = {
    0: "一萬", 1: "二萬", 2: "三萬", 3: "四萬", 4: "五萬", 5: "六萬", 6: "七萬", 7: "八萬", 8: "九萬",
    9: "一筒", 10: "二筒", 11: "三筒", 12: "四筒", 13: "五筒", 14: "六筒", 15: "七筒", 16: "八筒", 17: "九筒",
    18: "一索", 19: "二索", 20: "三索", 21: "四索", 22: "五索", 23: "六索", 24: "七索", 25: "八索", 26: "九索",
    27: "東", 28: "南", 29: "西", 30: "北",
    31: "白", 32: "發", 33: "中"
}

# 和了処理
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
                # time.sleep(1)  # 1秒遅延
                print()

    for lst in all_lists:
        lst.sort()

    return player_list, cp2_list, cp3_list, cp4_list

# 牌の表示関数
def display_tiles_by_id(tile_list):
    tiles = [mahjong_tiles.get(tile_id) for tile_id in tile_list]
    return " ".join(tiles)

class MahjongGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("麻雀牌")

        self.hand = []
        self.draw_button = tk.Button(self.root, text="牌を引く", command=self.draw_and_discard_tile)
        self.draw_button.pack()

        self.sort_button = tk.Button(self.root, text="手持ちの牌をソート", command=self.sort_hand)
        self.sort_button.pack()

        self.tiles_label = tk.Label(self.root, text="手持ちの牌:")
        self.tiles_label.pack()

        self.tiles_display = tk.Label(self.root, text="")
        self.tiles_display.pack()

        self.drawn_tile_label = tk.Label(self.root, text="")
        self.drawn_tile_label.pack()

        self.discard_label = tk.Label(self.root, text="")
        self.discard_buttons = []

        self.initial_draw(13)  # 最初に13枚の牌を配る

    def initial_draw(self, num_tiles):
        # 初期手札の配布
        for _ in range(num_tiles):
            tile_type = random.choice(list(mahjong_tiles.keys()))  # 牌の種類をランダムに選択
            tile = random.choice(list(mahjong_tiles.values()))  # 選択した種類の中から牌を選ぶ
            if self.hand.count(tile) < 4:  # 各牌を4つまでしか配らないようにする
                self.hand.append(tile)
        self.sort_hand()
        self.update_display()

    def draw_and_discard_tile(self):
        drawn_tile = random.choice(list(mahjong_tiles.values()))
        if self.hand.count(drawn_tile) < 4:
            self.hand.append(drawn_tile)
            self.update_display()

            # 引いた牌を表示
            self.drawn_tile_label.config(text=f"引いた牌: {drawn_tile}")

            self.sort_hand()  # 牌を引いた後に手持ちの牌をソートする
            self.update_display()  # ソート後の手持ちの牌を表示

            # 牌を捨てるラベルとボタンを更新
            self.update_discard_ui()


    def discard_selected_tile(self, selected_tile):
        self.hand.remove(selected_tile)
        self.update_display()
        self.update_discard_ui()

    def update_display(self):
        # スペースを挿入して引いた牌を表示
        display_hand = ", ".join(self.hand[:-1]) + f"  {self.hand[-1]}" if self.hand else ""
        self.tiles_display.config(text=display_hand)

    def update_discard_ui(self):
        if self.root is not None:
            self.discard_label.config(text="捨てる牌を選んでください:")
            for button in self.discard_buttons:
                button.destroy()

            self.discard_buttons = []
            for tile in self.hand:
                button = tk.Button(self.root, text=tile, command=lambda t=tile: self.discard_selected_tile(t))
                self.discard_buttons.append(button)
                button.pack()
    
    def sort_hand(self):
        self.hand.sort()
        self.update_display()  # ソート後の手持ちの牌を更新


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = MahjongGame()
    game.run()
