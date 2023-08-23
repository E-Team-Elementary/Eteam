const publicEditModal = document.getElementById("edit-modal");
const publicEditBtn = document.getElementById("edit-channel");
const publicEditName = document.getElementById("edit-public-name");
const publicDescription = document.getElementById("editDescription");

const editForm = document.getElementById("edit-name");

function editChannel(channel_id, channel_name, channel_description) {

  //alert(channel_name);
  //alert(channel_description);
  publicEditModal.style.display = "flex";
  const inputHiddenElement = document.createElement("input");
  inputHiddenElement.type = "hidden";
  inputHiddenElement.id = "public_edit_channel_id";
  inputHiddenElement.value = channel_id;
  publicEditName.value = channel_name;
  publicDescription.value = channel_description
  editForm.insertBefore(inputHiddenElement, publicEditName, publicDescription, editForm.firstChild);
}

addEventListener("click", (e) => {
  if (e.target == publicEditModal) {
    publicEditModal.style.display = "none";
    const editElement = document.getElementById("public_edit_channel_id");
    editForm.removeChild(editElement);
  }
});

