"use strict";

$(document).ready(function () {
    var $grid = $('.grid').masonry({
        itemSelector: '.grid-item',
        columnWidth: 275,
        gutter: 10
    });

    $grid.imagesLoaded().progress(function() {
      $grid.masonry('layout');
    });
});
