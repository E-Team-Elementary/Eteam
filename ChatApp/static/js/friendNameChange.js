// フレンドチャットのタイトルはログインユーザーとフレンドの名前の結合した文字列になっている
// 例 taro:jiro
// ログインユーザーの名前を除き、見た目を変更する為の処理

// フレンドの数
friend_volume = document.getElementById("friend_volume");

// サイドバーの表示をフレンドの名前のみに変更する処理
for (let i = 0; i < friend_volume.value; i++) {
  let id = "friend-name" + i;
  let bindName = document.getElementById(id).innerHTML;

  const nameSplit = bindName.split(":");

  if (user_name == nameSplit[0]) {
    document.getElementById(id).innerHTML = nameSplit[1];
  } else {
    document.getElementById(id).innerHTML = nameSplit[0];
  }
}

// フレンド毎のチャット上部にあるタイトルの修正
const title = document.getElementById("channel_name_title");

// タイトルはTOPページには無いため、処理をしない為の分岐
if (title) {
  const titleSplit = title.innerHTML.split(":");

  if (user_name == titleSplit[0]) {
    document.getElementById("channel_name_title").innerHTML = titleSplit[1];
  } else {
    document.getElementById("channel_name_title").innerHTML = titleSplit[0];
  }
}
