!(function(){

    var $goldGrid = $('#gold-grid');
    var $silverGrid = $('#silver-grid');
    var $bronzeGrid = $('#bronze-grid');

    //larger company grid
    if($goldGrid){
      $goldGrid.imagesLoaded(function(){
        $goldGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }
    if($silverGrid){
      $silverGrid.imagesLoaded(function(){
        $silverGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }
    if($bronzeGrid){
      $bronzeGrid.imagesLoaded(function(){
        $bronzeGrid.masonry({
          'gutter': 0,
          'itemSelector': '.company-card',
        });
      });
    }

})(jQuery);