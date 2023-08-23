message = document.getElementById("flashMessage").value;

if (message) {
  Swal.fire({
    icon: "success",
    text: message,
  });
}
