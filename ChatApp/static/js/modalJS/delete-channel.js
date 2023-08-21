const publicDeleteModal = document.getElementById("delete-public-modal");
const publicDeleteBtn = document.getElementById("trash-channel");

if (publicDeleteModal) {

  // When the user clicks the button, open the modal.
    publicDeleteBtn.onclick = function() {
    publicDeleteModal.style.display = 'flex';
  };

  addEventListener("click", (e) => {
    if (e.target == publicDeleteModal) {
    publicDeleteModal.style.display = "none";
    }
  });
}