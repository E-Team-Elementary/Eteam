const publicDeleteModal = document.getElementById("delete-public-modal");
const publicDeleteBtn = document.getElementById("trash-channel");

const deleteForm = document.getElementById("public-channel-delete");

function deleteChannel(channel_id) {
  publicDeleteModal.style.display = "flex";
  const inputHiddenElement = document.createElement("input");
  inputHiddenElement.type = "hidden";
  inputHiddenElement.id = "public_delete_channel_id";
  inputHiddenElement.value = channel_id;
  deleteForm.insertBefore(inputHiddenElement, deleteForm.firstChild);
}

addEventListener("click", (e) => {
  if (e.target == publicDeleteModal) {
    publicDeleteModal.style.display = "none";
    const deleteElement = document.getElementById("public_delete_channel_id");
    deleteForm.removeChild(deleteElement);
  }
});
