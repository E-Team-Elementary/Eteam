const addModal = document.getElementById("add-modal");
const addBtn = document.getElementById("open-modal");

if (addModal) {
  // When the user clicks the button, open the modal.
  addBtn.onclick = function () {
    addModal.style.display = "flex";
  };

  addEventListener("click", (e) => {
    if (e.target == addModal) {
      addModal.style.display = "none";
    }
  });
}

let result = document.getElementById("searched-user");
let form = document.getElementById("friend-search-form");
let sendButton = document.getElementById("friend-request-button");
let userData;

form.addEventListener("submit", function (event) {
  event.preventDefault();

  let emailData = new FormData(form);

  const xhr1 = new XMLHttpRequest();
  xhr1.open("POST", "/search_user");
  xhr1.send(emailData);

  xhr1.onload = function () {
    if (xhr1.status == 200) {
      // モーダル内にメッセージを表示
      userData = JSON.parse(xhr1.responseText);
      result.innerHTML = "<p>ユーザー名: " + userData.user_name + "</p>";
      result.innerHTML += "<p>メールアドレス: " + userData.email + "</p>";
      sendButton.style.display = "block";
    } else {
      result.innerHTML = "<p>ユーザーが見つかりませんでした。</p>";
    }
  };
});

// ボタンがクリックされたときの処理を定義
sendButton.addEventListener("click", function () {
  const xhr2 = new XMLHttpRequest();

  xhr2.open("POST", "/friend_request", true);
  xhr2.setRequestHeader("Content-Type", "application/json");

  const data = {
    receiver_id: userData.user_id,
  };
  const jsonData = JSON.stringify(data);

  xhr2.send(jsonData);

  xhr2.onreadystatechange = function () {
    if (xhr2.readyState === XMLHttpRequest.DONE) {
      if (xhr2.status === 200) {
        // サーバーサイドからのリダイレクト情報を使用してリダイレクト
        const redirectURL = xhr2.getResponseHeader("X-Redirect");
        if (redirectURL) {
          window.location.href = redirectURL;
        }
      } else {
        console.error("POSTリクエストが失敗しました。");
      }
    }
  };
});
