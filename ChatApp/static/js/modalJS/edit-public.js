//  モーダルエリアの取得
const publicEditModal = document.getElementById("edit-modal");

// 編集モーダルの入力欄の要素を取得
const publicEditName = document.getElementById("edit-public-name");
const publicDescription = document.getElementById("editDescription");

// formエリアの取得
const editForm = document.getElementById("edit-name");

//  編集ボタン押下時のイベント
function editChannel(channel_id, channel_name, channel_description) {
  //  モーダルエリアの表示
  publicEditModal.style.display = "flex";

  //  モーダルを開いた際に動的に変更するchannel_idをinput hiddenに保持する
  const inputHiddenElement = document.createElement("input");
  inputHiddenElement.type = "hidden";
  inputHiddenElement.name = "channel_id";
  inputHiddenElement.id = "public_edit_channel_id";
  inputHiddenElement.value = channel_id;
  editForm.insertBefore(inputHiddenElement, editForm.firstChild);

  // 現在のチャンネルタイトル、チャンネル説明文を入力欄に初期表示する
  publicEditName.value = channel_name;
  publicDescription.value = channel_description;
}

addEventListener("click", (e) => {
  if (e.target == publicEditModal) {
    publicEditModal.style.display = "none";
    const editElement = document.getElementById("public_edit_channel_id");
    editForm.removeChild(editElement);
  }
});
