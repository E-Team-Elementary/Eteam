message = document.getElementById("flashMessage");

if (message) {
  Swal.fire({
    icon: "success",
    text: message.value,
  });
}
