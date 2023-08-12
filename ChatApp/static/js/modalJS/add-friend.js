const addModal = document.getElementById('add-modal');
const addBtn = document.getElementById('open-modal');

if (addModal) {

  // When the user clicks the button, open the modal.
    addBtn.onclick = function() {
    addModal.style.display = 'flex';
  };

  addEventListener("click", (e) => {
    if (e.target == addModal) {
      addModal.style.display = "none";
    }
  });
}