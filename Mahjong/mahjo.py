import random
import time
import hashlib
import time
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig

# マージャンの牌の種類とその番号の対応
mahjong_tiles = {
    0: "一萬", 1: "二萬", 2: "三萬", 3: "四萬", 4: "五萬", 5: "六萬", 6: "七萬", 7: "八萬", 8: "九萬",
    9: "一筒", 10: "二筒", 11: "三筒", 12: "四筒", 13: "五筒", 14: "六筒", 15: "七筒", 16: "八筒", 17: "九筒",
    18: "一索", 19: "二索", 20: "三索", 21: "四索", 22: "五索", 23: "六索", 24: "七索", 25: "八索", 26: "九索",
    27: "東", 28: "南", 29: "西", 30: "北",
    31: "白", 32: "發", 33: "中"
}

# 萬子の名称に対応する辞書
manzu_dict = {
    "一萬": 1, "二萬": 2, "三萬": 3, "四萬": 4, "五萬": 5, "六萬": 6, "七萬": 7, "八萬": 8, "九萬": 9
}

# 索子の名称に対応する辞書
souzu_dict = {
    "一索": 1, "二索": 2, "三索": 3, "四索": 4, "五索": 5, "六索": 6, "七索": 7, "八索": 8, "九索": 9
}

# 筒子の名称に対応する辞書
pinzu_dict = {
    "一筒": 1, "二筒": 2, "三筒": 3, "四筒": 4, "五筒": 5, "六筒": 6, "七筒": 7, "八筒": 8, "九筒": 9
}

# 字牌の名称に対応する辞書
ji_dict = {
    "東": 1, "南": 2, "西": 3, "北": 4, "白": 5, "發": 6, "中": 7
}

player_name = {
    1 : 'player', 2 : 'cp1', 3 : 'cp2'
}

#3人麻雀
player=[] #自分
cp1=[]
cp2=[]
discard_tile=[]


#和了処理
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig

#結果表示
def print_hand_result(hand_result):
    print(hand_result.han, hand_result.fu)
    print(hand_result.cost['main'], hand_result.cost['additional'])
    print(hand_result.yaku)
    for fu_item in hand_result.fu_details:
        print(fu_item)
    print('')

#ツモの設定
def calculate_tsumo(tiles, win_tile, melds=None, dora_indicators=None):
    calculator = HandCalculator()
    config = HandConfig(is_tsumo=True)  # ツモの設定を追加

    result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)
    print_hand_result(result)

# 和了処理呼び出し
def result(lst, tumo):
    pais=lst
    man,pin,sou,honor=count_pai_types(pais)

    tm=mahjong_tiles[tumo[0]]
    if tm in manzu_dict:
        mans = str(manzu_dict[tm])
        win_tile = TilesConverter.string_to_136_array(man=mans)[0]
    elif tm in souzu_dict:
        sous = str(souzu_dict[tm])
        win_tile = TilesConverter.string_to_136_array(sou=sous)[0]
    elif tm in pinzu_dict:
        pins = str(pinzu_dict[tm])
        win_tile = TilesConverter.string_to_136_array(pin=pins)[0]
    elif tm in ji_dict:
        honors = str(ji_dict[tm])
        win_tile = TilesConverter.string_to_136_array(honor=honors)[0]

    tiles = TilesConverter.string_to_136_array(man=man, pin=pin, sou=sou)
    
    melds = None
    dora_indicators = None

    return calculate_tsumo(tiles, win_tile, melds, dora_indicators)



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
def distribute_tiles(original_list, player_list, cp2_list, cp3_list):
    all_lists = [player_list, cp2_list, cp3_list]

    for i, tile in enumerate(original_list):
        current_list = all_lists[i % 3]
        if len(current_list) < 13:
            current_list.append(tile)
            if current_list is player_list:  # playerの手札が配られる場合
                display_tiles_by_id(player_list)  # playerの牌を表示

    for lst in all_lists:
        lst.sort()

    return player_list, cp2_list, cp3_list

# 牌の表示関数
def display_tiles_by_id(tile_list):
    tile_list.sort()
    tiles = [mahjong_tiles.get(tile_id) for tile_id in tile_list]
    return " ".join(tiles)

# 牌のidから文字リストへ変更関数
def translate_tiles_by_id(tile_list):
    tile_list.sort()
    tiles = [mahjong_tiles.get(tile_id) for tile_id in tile_list]
    return tiles  # 牌の名前のリストを返す

def count_pai_types(pai):
    mans = pins = sous = honors = ''

    # 各種類の牌の数をカウント
    for p in pai:
        if p in manzu_dict:
            mans += str(manzu_dict[p])
        elif p in souzu_dict:
            sous += str(souzu_dict[p])
        elif p in pinzu_dict:
            pins += str(pinzu_dict[p])
        elif p in ji_dict:
            honors += str(ji_dict[p])

    return mans, pins, sous, honors

def cp_move(lst,pai_yama):
    lst.append(pai_yama.pop()) #ツモ
    cp_list=shuffle_list_with_random_seed(lst) #捨て牌
    cp_out=cp_list.pop()
    discard_tile.append(cp_out)
    cp_outlst=cp_list.sort()
    return cp_outlst

def get_list(number):
    if number == 1:
        return player
    elif number == 2:
        return cp1
    elif number == 3:
        return cp2
    

def player_move(lst, pai_yama):
    # ツモ
    tumo = []
    tumo.append(pai_yama.pop())
    print(display_tiles_by_id(tumo), 'を引きました')

    print(display_tiles_by_id(player)," ",display_tiles_by_id(tumo))

    action = input("和了する場合は '和了' と入力してください。牌を捨てる場合は'打牌'と入力してください:")
    
    if action == '和了':
        # 和了する場合
        # result 関数に player の手牌とツモを送る
        result(lst, tumo)
    else:
        # 牌を捨てる場合
        print("捨てる牌を選んでください:")
        print(display_tiles_by_id(player)," ",display_tiles_by_id(tumo))
        discard = input("\n捨てる牌を選んでください（例: 一萬）:")
        
        # 捨てる牌の取得
        for tile_id, tile_name in mahjong_tiles.items():
            if tile_name == discard:
                discard_tiles = int(tile_id)
                break
        
        sw=False
        while sw==False:
            if discard_tiles in lst:
                lst.remove(discard_tiles)
                discard_tile.append(discard_tiles)
                print(f"{discard} を捨てました")
                sw=True
            elif tumo==discard_tiles:
                discard_tile.append(discard_tiles)
                print(f"{discard} を捨てました")
                sw=True
            else:
                print("その牌は手持ちにありません")
        
        return lst

#==================ここからスタート
place=[1, 2, 3]
order = shuffle_list_with_random_seed(place)

#牌山の生成
pai = [i for i in range(34) for _ in range(4)]  # 牌のリスト（136枚）
pai_yama = shuffle_list_with_random_seed(pai)
print(pai_yama)

#3人麻雀
player=[] #自分
cp1=[]
cp2=[]
discard_tile=[]

#牌山の牌を3人に配布
distribute_tiles(pai_yama,player,cp1,cp2)

#tumo=[]
#tumo.append(pai_yama.pop())
#print(tumo)
#result(player, tumo)



c=1
cc=1
#===対局開始
for _ in range(3):
    while True:
        print('-------------------------------------------')
        #一人目
        time.sleep(3)
        if c==3:
            print('オーラス')
        else:
            print('第',c,'局')
        time.sleep(1)
        print('『',cc,'』巡目')
        time.sleep(3)
        print(f"次のプレイヤーは {player_name[order[0]]} 番です。")
        print('捨て牌一覧:',display_tiles_by_id(discard_tile),'\n')
        time.sleep(3)
        if player_name[order[0]]=='player':
            player_move(player, pai_yama)
        else:
            cp_move(get_list(order[0]),pai_yama)

        #二人目
        print('-------------------------------------------')
        time.sleep(3)
        print('『',cc,'』巡目')
        time.sleep(3)
        print(f"次のプレイヤーは {player_name[order[1]]} 番です。")
        print('捨て牌一覧:',display_tiles_by_id(discard_tile),'\n')
        time.sleep(3)
        if player_name[order[1]]=='player':
            player_move(player, pai_yama)
        else:
            cp_move(get_list(order[1]),pai_yama)

        #三人目
        print('-------------------------------------------')
        time.sleep(3)
        print('『',cc,'』巡目')
        time.sleep(3)
        print(f"次のプレイヤーは {player_name[order[2]]} 番です。")
        print('捨て牌一覧:',display_tiles_by_id(discard_tile),'\n')
        time.sleep(3)
        if player_name[order[2]]=='player':
            player_move(player, pai_yama)
        else:
            cp_move(get_list(order[2]),pai_yama)
    
        cc+=1
    c+=1