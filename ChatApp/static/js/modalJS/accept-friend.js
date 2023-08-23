const acceptModal = document.getElementById("request-modal");
const acceptBtn = document.getElementById("request-friends");

if (acceptModal) {
  // When the user clicks the button, open the modal.
  acceptBtn.onclick = function () {
    acceptModal.style.display = "flex";
  };

  // When the user clicks outside the modal -- close it.
  window.onclick = function (event) {
    if (event.target == acceptModal) {
      // Which means he clicked somewhere in the modal (background area), but not target = modal-content
      acceptModal.style.display = "none";
    }
  };
}

// フレンド申請一覧を取得
const xhr3 = new XMLHttpRequest();

xhr3.open("GET", "/friend_request", true);
xhr3.responseType = "json";

xhr3.onload = function () {
  const data2 = xhr3.response;
  const select = document.getElementById("friend-request");
  select.options.length = 0;

  for (let request of data2) {
    const option = document.createElement("option");
    option.value = request.sender_id;
    const date = new Date(request.created_at);
    const formattedDate = `${date.getFullYear()}/${
      date.getMonth() + 1
    }/${date.getDate()}`;
    option.textContent = `${request.sender_name} (${formattedDate})`;
    select.appendChild(option);
  }
};
xhr3.send();

// 承認・拒否ボタンの表示切り替え
const friendRequest = document.getElementById("friend-request");
const allButton = document.getElementById("all-button");

friendRequest.addEventListener("change", () => {
  const selectedOption = friendRequest.options[friendRequest.selectedIndex];

  if (selectedOption.value !== "") {
    allButton.style.display = "block"; // ボタンを表示
  } else {
    allButton.style.display = "none"; // ボタンを非表示
  }
});

friendRequest.addEventListener("click", (e) => {
  const isOption = e.target.tagName === "OPTION";
  if (isOption) {
    allButton.style.display = "block";
  }
});
document.addEventListener("click", (e) => {
  const isOption = friendRequest.contains(e.target);
  if (!isOption) {
    allButton.style.display = "none";
  }
});

// フレンド申請　承認・拒否送信
const acceptButton = document.getElementById("accept-button");
const denyButton = document.getElementById("deny-button");

acceptButton.addEventListener("click", () => {
  const selectedOption = friendRequest.options[friendRequest.selectedIndex];
  const senderId = selectedOption.value;
  sendFriendResponse(senderId, "accept");
});

denyButton.addEventListener("click", () => {
  const selectedOption = friendRequest.options[friendRequest.selectedIndex];
  const senderId = selectedOption.value;
  sendFriendResponse(senderId, "deny");
});

function sendFriendResponse(senderId, response) {
  const xhr4 = new XMLHttpRequest();
  xhr4.open("POST", "/friend-response", true);
  xhr4.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  const data = {
    sender_id: senderId,
    response: response,
  };
  const jsonData = JSON.stringify(data);

  xhr4.onreadystatechange = function () {
    if (xhr4.readyState === XMLHttpRequest.DONE) {
      if (xhr4.status === 200) {
        // サーバーサイドからのリダイレクト情報を使用してリダイレクト
        const redirectURL = xhr4.getResponseHeader("X-Redirect");
        if (redirectURL) {
          window.location.href = redirectURL;
        }
      } else {
        console.error("POSTリクエストが失敗しました。");
      }
    }
  };

  xhr4.send(jsonData);
}
