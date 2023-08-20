window.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("button_search")
    .addEventListener("click", function () {
      let p_elements = document.querySelectorAll("p");
      let search_word = document.getElementById("search_word").value;
      let reg = new RegExp(search_word, "gi");

      if (!search_word || search_word.length == 0) {
        console.log("文字列は空です");
      } else {
        for (let pi = 0; pi < p_elements.length; pi++) {
          let p_text = p_elements[pi].textContent;

          p_elements[pi].innerHTML = p_text.replace(reg, function (match_word) {
            return "<em>" + match_word + "<em>";
          });
        }
        let search_word_first = document.querySelector("em");
        search_word_first.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
});
