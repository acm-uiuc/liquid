/*
    Controller code for the Banks of the boneyard blog
*/


(function(){


    var targets = {
      'id_title' : 'post-title-preview',
      'id_content_markdown' : 'post-content-preview'
    };




    //LOAD
    $(document).ready(function(){

      reset_text();

      //EVENTS
      $('#id_title').keyup(gen_preview);//('keyup', gen_preview(e));
      $('#id_content_markdown').on('keyup', gen_preview);

    });


    function reset_text(){
      for(var key in targets){
        var source = $('#'.concat(key));
        if( source && source.val() !== ''){
          gen_preview(source);
        }
      }
    }

    // Generates the markdonw preview from the given field
    // Can be passed an event object or a jQuery object
    function gen_preview(e){
      var source = e.target !== undefined ? $(e.target) : e;
      var targetId = '#'.concat(targets[source.attr("id")]);

      $(targetId).html(markdown.toHTML(source.val()));

    }

})();

