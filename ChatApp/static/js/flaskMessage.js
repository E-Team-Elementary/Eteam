// flashメッセージがある時に、アラート起動する

const flashMessage = document.getElementById("flashMessage");

if (flashMessage) {
  const splitFlashMessage = flashMessage.value.split(":");

  // NG系のアラートはアイコンをバツマークで表示させる
  if ("NG" == splitFlashMessage[0]) {
    Swal.fire({
      icon: "error",
      text: splitFlashMessage[1],
    });
  } else {
    Swal.fire({
      icon: "success",
      text: splitFlashMessage[1],
    });
  }
}
