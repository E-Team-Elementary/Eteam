const deletePageButtonClose = document.getElementById(
  "delete-page-close-button"
);
const deleteChannelConfirmButton = document.getElementById(
  "delete-channel-confirmation-button"
);

const deleteChannelButton = document.getElementById("delete-channel-button");

const deleteChannelModal = document.getElementById("delete-channel-modal");

deleteChannelButton.addEventListener("click", () => {
  deleteChannelModal.style.display = "flex";
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener("click", (e) => {
  if (e.target == deleteChannelModal) {
    deleteChannelModal.style.display = "none";
  }
});
