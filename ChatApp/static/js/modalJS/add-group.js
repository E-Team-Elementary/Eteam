const groupModal = document.getElementById('group-modal');
const groupBtn = document.getElementById('add-group');

if (groupModal) {

  // When the user clicks the button, open the modal.
    groupBtn.onclick = function() {
    groupModal.style.display = 'flex';
  };

  addEventListener("click", (e) => {
    if (e.target == groupModal) {
      groupModal.style.display = "none";
    }
  });
}

