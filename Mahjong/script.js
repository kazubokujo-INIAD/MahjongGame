// 牌山のリストを生成する関数
function createMahjongDeck() {
    const mahjongTiles = [
      // 萬子
      "1萬", "2萬", "3萬", "4萬", "5萬", "6萬", "7萬", "8萬", "9萬",
      // 筒子
      "1筒", "2筒", "3筒", "4筒", "5筒", "6筒", "7筒", "8筒", "9筒",
      // 索子
      "1索", "2索", "3索", "4索", "5索", "6索", "7索", "8索", "9索",
      // 風牌
      "東", "南", "西", "北",
      // 三元牌
      "白", "發", "中"
    ];
  
    // 牌山のリストを初期化
    let deck = [];
  
    // 各牌に対応する数だけ牌山に追加
    mahjongTiles.forEach(tile => {
      // 例えば1萬は4枚、他の牌はそれぞれ4枚ずつとして追加
      let count = 4; // 1萬以外の牌の初期数
      if (tile.startsWith("1")) {
        count = 4; // 1萬の数
      }
      for (let i = 0; i < count; i++) {
        deck.push(tile);
      }
    });
  
    return deck;
  }
  
  // 牌山を生成
  const mahjongDeck = createMahjongDeck();
  console.log(mahjongDeck); // 生成された牌山のリストを表示
  