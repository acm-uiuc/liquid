!(function(){

    var $goldGrid = $('#gold-grid');
    var $silverGrid = $('#silver-grid');
    var $bronzeGrid = $('#bronze-grid');

    //larger company grid
    if($goldGrid.length){
      $goldGrid.imagesLoaded(function(){
        $goldGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }
    if($silverGrid.length){
      $silverGrid.imagesLoaded(function(){
        $silverGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }
    if($bronzeGrid.length){
      $bronzeGrid.imagesLoaded(function(){
        $bronzeGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }

})(jQuery);