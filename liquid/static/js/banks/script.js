
//global converter
converter = new Showdown.converter();

$(document).ready(function(){
  var that = this;

  //automatically render all content
  renderText($('#id_title'), $('#titlePreview'));
  renderText($('#id_subtitle'), $('#subtitlePreview'));
  renderMarkdown($('#id_content_markdown'), $('#markupPreview'));

  //render title on input
  $('#id_title').keyup(function(e){
    renderText($(this), $('#titlePreview') );
  });

  $('#id_subtitle').keyup(function(e){
    renderText($(this), $('#subtitlePreview'));

  });

  //listen for input on markdown tab
  $('#id_content_markdown').keyup(function(){
     renderMarkdown($(this), $('#markupPreview'));
  });

});

function renderText(source, target){
  target.empty();
  target.html(source.val());
}

function renderMarkdown(source, target){
    var md = source.val();
    var markup = converter.makeHtml(md);
    target.empty();
    target.html(markup);
}

