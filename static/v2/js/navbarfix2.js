
(function($) {
    var $window = $(window),
        $html = $('html');

    function resize() {
        if ($window.width() < 991) {
           $("#sidecontent").attr("id", "sifnewid");
        }

        $("#sidecontent").attr("id", "sidecontent");
    }

    $window.resize(resize).trigger('resize');
})(jQuery);


(function($) {
  var top = $('#sidecontent').offset().top - parseFloat($('#sidecontent').css('marginTop').replace(/auto/, 0));
  var footTop = $('#footer').offset().top - parseFloat($('#footer').css('marginTop').replace(/auto/, 0));

  var maxY = footTop - $('#sidecontent').outerHeight();

  $(window).scroll(function(evt) {
    var y = $(this).scrollTop();
    if (y > top) {
      if (y < maxY) {
        $('#sidecontent').addClass('fixed').removeAttr('style');
      } else {
        $('#sidecontent').removeClass('fixed').css({
          position: 'absolute',
          top: (maxY - top) + 'px'
        });
      }
    } else {
      $('#sidecontent').removeClass('fixed');
    }
  });
})(jQuery);
