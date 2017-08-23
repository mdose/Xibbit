"use strict";


function toggleButton(evt) {
    // Specifically toggles button from empty to filled star
    // AJAX success function
    var glyphicon = $("#favorite");
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
    // Favor and unfavor Art to the DB on the UserArt Table

    evt.preventDefault();
    // keeps page from reloading right away

    var art_id = $("#hidden_art_id").val();
    // passes (unique) art_id from jinja/html to js using the .val() func
    $.get("/toggle/art.json", {"art_id": art_id}, toggleButton);
    //AJAX get request: goes to special /toggle route (to avoid confusion of 
    // "/artworks/" + $("#hidden_art_id").val() + ".json" URL complexities to Flask), 
    // passes OPTIONAL get info to the server (here we pass the art_id pulled from Jinja
    // as a dictionary [which doesn't need to be "sanitized" b/c the user never touches it]),
    // and lastly declare the success funtion that will happen once info is returned from the server
}

function toggleFavoriteArtist(evt) {
    // Favor and unfavor Artist to the DB on the UserArtist Table

    evt.preventDefault();

    var artist_id = $("#hidden_artist_id").val();

    $.get("/toggle/artist.json", {"artist_id": artist_id}, toggleButton);
}

function toggleFavoriteCollection(evt) {
    // Favor and unfavor Collections to the DB on the UserCollection Table

    evt.preventDefault();

    var collection_id = $("#hidden_collection_id").val();

    $.get("/toggle/collection.json", {"collection_id": collection_id}, toggleButton);
}

$(document).ready(function () {
    // AJAX EventListener: When 'click' on fav btn, initiate toggleFavoriteArt func 
    $('#favorite-art-btn').on('click', toggleFavoriteArt);
});

$(document).ready(function () {
    // AJAX EventListener: When 'click' on fav btn, initiate toggleFavoriteArtist func 
    $('#favorite-artist-btn').on('click', toggleFavoriteArtist);
});

$(document).ready(function () {
    // AJAX EventListener: When 'click' on fav btn, initiate toggleFavoriteCollection func 
    $('#favorite-collection-btn').on('click', toggleFavoriteCollection);
});