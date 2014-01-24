function show_event(id){
  $("#event-"+id).show();
  $("#event-details").modal("show")
}

function close_event() {
  window.location.hash = "index";
}

function load_from_hash(){
  var id = window.location.hash.split('/')[1];
  if (typeof id != 'undefined') {
    show_event(id);
  }
}

$(document).ready(function(){

  $("#event-details").on('hidden', function () {
    $(".event-details-inner").hide();
    close_event();
  });

  $(window).bind('hashchange', function() {
    load_from_hash();
  });

  if(window.location.hash != ""){
    load_from_hash();
  }
});
