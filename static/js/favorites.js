"use strict";


function toggleButton(evt) {
    // Specifically toggles button from empty to filled star
    // AJAX success function
    var glyphicon = $("#unfavorited");
    // JQUERY looks at the span (not button), since that's what's changing
    
    if (glyphicon.hasClass('glyphicon-star-empty')) {
        // if not favorited yet, fill star to mark as faved after click
        glyphicon.removeClass('glyphicon-star-empty');
        glyphicon.addClass('glyphicon-star');
    }

    else {
        // if filled star and clicked; revert to empty star
        glyphicon.removeClass('glyphicon-star');
        glyphicon.addClass('glyphicon-star-empty');
    }
}

function toggleFavoriteArt(evt) {
    // Add favorited Art to the DB on the UserArt Table

    evt.preventDefault();
    // keeps page from reloading right away

    var art_id = $("#hidden_art_id").val() 
    // passes (unique) art_id from jinja/html to js using the .val() func
    $.get("/toggle.json", {"art_id": art_id}, toggleButton};
    //AJAX get request: goes to special /toggle route (to avoid confusion of 
    // "/artworks/" + $("#hidden_art_id").val() + ".json" URL complexities to Flask), 
    // passes OPTIONAL get info to the server (here we pass the art_id pulled from Jinja
    // as a dictionary [which doesn't need to be "sanitized" b/c the user never touches it]),
    // and lastly declare the success funtion that will happen once info is returned from the server
}

$(document).ready(function () {
    // AJAX EventListener: When 'click' on fav btn, initiate toggleFavoriteArt func 
    $('#favorite-btn').on('click', toggleFavoriteArt);
});