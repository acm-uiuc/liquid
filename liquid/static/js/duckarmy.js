var code = "duckarmy"
var codeArr = 0

$("body").keypress(function(e) {
  var c = String.fromCharCode(e.which);
  if (codeArr < code.length && c == code[codeArr])
    codeArr++

  if (codeArr >= code.length) {
    console.log("dux");
    $(this).append("<iframe id='duckvid' width='1' height='1' src='https://www.youtube.com/embed/nHc288IPFzk?autoplay=1&start=4' frameborder='0'></iframe>");
    codeArr = 0;
    setTimeout(function(){
        $("#duckvid").remove();
    }, 9500);
  }
});
