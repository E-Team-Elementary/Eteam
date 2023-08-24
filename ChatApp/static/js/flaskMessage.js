const flashMessage = document.getElementById("flashMessage");

if (flashMessage) {
  Swal.fire({
    icon: "success",
    text: flashMessage.value,
  });
}
