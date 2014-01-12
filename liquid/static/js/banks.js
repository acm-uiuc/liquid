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

      $('#id_title').on('keyup', function(e){
        var target = $(e.target);
        gen_preview(target.val(), targets[target.attr('id')]);
      });

      $('#id_content_markdown').on('keyup', function(e){
        var target = $(e.target);
        gen_preview(target.val(), targets[target.attr('id')]);
      });


    });




    function gen_preview(content, targetId){
      idString = "#".concat(targetId);
      console.log("iD: " + idString);

      $(idString).html(markdown.toHTML(content));

    };

})();

