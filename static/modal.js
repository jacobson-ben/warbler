$('#pop-modal').on('click', createModal)
$('#make-a-warble').on('submit', submitWarble)

function createModal(evt){
  evt.preventDefault();
  $('#pop-up-modal').show()
}


async function submitWarble(evt) {
  evt.preventDefault();
  let text = $("#warble-text").val()
  response = await axios.post("/messages/new", {text})
  warble = response.data
}
