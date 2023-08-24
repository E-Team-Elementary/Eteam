function checkForm() {
  const message = document.getElementById("input-check-message");
  const name = document.getElementById("input-group-name");
  const friends = document.getElementsByName("friends");

  // チャンネル名入力チェック
  if (name.value == "") {
    message.innerHTML = "チャンネル名は入力してください";
    return false;
  }
  // チェックボックスが1つ以上選ばれているかチェック
  let checkedFlg = false;

  for (let i = 0; i < friends.length; i++) {
    if (friends[i].checked) {
      checkedFlg = true;
      break;
    }
  }

  if (!checkedFlg) {
    message.innerHTML = "メンバーを1人以上選択してください";
    return false;
  }

  return true;
}
