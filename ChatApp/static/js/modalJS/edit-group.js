//  モーダルエリアの取得
const publicEditModal = document.getElementById("edit-modal");

// ボタンの取得
const editButton = document.getElementById("edit-channel-button");

// モーダルの表示
editButton.addEventListener("click", () => {
  publicEditModal.style.display = "flex";
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener("click", (e) => {
  if (e.target == publicEditModal) {
    publicEditModal.style.display = "none";
  }
});
