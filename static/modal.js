$('#pop-modal').on('click', createModal)

function createModal(evt){
  evt.preventDefault();
  console.log('hi')
  let createHTML = appendHtmlToModal();
  $('#to-append-modal').append(createHTML);
  
}

function appendHtmlToModal(){
  return `
  <div class="modal show" id="myModal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">Modal Header</h4>
        </div>
        <form>
        <div class="modal-body">
           <input id="warble-text" type="text" placeholder="create warble">
        </div>
        <div class="modal-footer">
          <button type="submit" class="btn btn-default" data-dismiss="modal">Add Warble</button>
        </div>
        </form>
      </div>
    </div>
  </div>
         
       
  `
}