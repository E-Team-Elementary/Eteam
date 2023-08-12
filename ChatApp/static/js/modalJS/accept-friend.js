const acceptModal = document.getElementById('request-modal');
const acceptBtn = document.getElementById('request-friends');

if (acceptModal) {

  // When the user clicks the button, open the modal.
    acceptBtn.onclick = function () {
    acceptModal.style.display = 'flex';
  };



  // When the user clicks outside the modal -- close it.
  window.onclick = function(event) {
    if (event.target == acceptModal) {
      // Which means he clicked somewhere in the modal (background area), but not target = modal-content
      acceptModal.style.display = 'none';
    }
  };
}