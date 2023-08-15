const publicModal = document.getElementById('public-modal');
const publicBtn = document.getElementById('open-add-public');

if (publicModal) {

  // When the user clicks the button, open the modal.
    publicBtn.onclick = function() {
    publicModal.style.display = 'flex';
  };

  addEventListener("click", (e) => {
    if (e.target == publicModal) {
      publicModal.style.display = "none";
    }
  });
}

