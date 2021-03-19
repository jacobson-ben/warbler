$('#pop-modal').on('click', createModal)
$('#make-a-warble').on('submit', submitWarble)

function createModal(evt){
  evt.preventDefault();
  $('#pop-up-modal').show()
}


async function submitWarble(evt) {
  evt.preventDefault();
  let text = $("#warble-text").val();
  let response = await axios.post("/messages/new", {text});
  let warble = response.data;
  let htmlToAppend = createWarbleHTML(warble);
  $("#messages").prepend(htmlToAppend);
  $("#make-a-warble").empty();
  $('#pop-up-modal').hide();
}

function createWarbleHTML(warble) {
  return `
    <li class="list-group-item">
          <a href="/messages/${warble.warble.id}" class="message-link"></a>

          <a href="/users/${warble.user.id}">
            <img src="${warble.user.user_image_url}" alt="user image" class="timeline-image">
          </a>

          <div class="message-area">
            <a href="/users/${warble.user.id}">@${warble.user.username}</a>
            <span class="text-muted">
              ${warble.warble.timestamp}
            </span>
            <p>${warble.warble.text}</p>
          </div>
  </li>
  `

}

