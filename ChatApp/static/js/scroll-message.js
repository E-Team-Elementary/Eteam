window.onload = function () {
  const scroller = document.getElementById("message-area");
  scroller.scrollTop = scroller.scrollHeight - scroller.clientHeight;

  const scroller2 = document.getElementById("note-area");
  scroller2.scrollTop = scroller2.scrollHeight - scroller2.clientHeight;

  const search_delete = document.getElementById("delete_search");
  search_delete.style.visibility = "hidden";
};
