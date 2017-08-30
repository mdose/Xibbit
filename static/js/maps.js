"use strict";

// TODO: ? var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 54.5260, lng: 15.2551},
        // Europe Coordinates ^
        // center: {lat: 27.467830, lng: -51.000000},
        // World Coordinates; zoom: 2
        // TODO: calc centerpt of all markers
        zoom: 4
    });

    getMarkersInfo(map, function(markers) {
        console.log(markers); // debug info
        var markerCluster = new MarkerClusterer(map, markers,
        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    });
}

function getMarkersInfo(map, cb_done) {
    $.get('/get_info', function(results) {
        var markers = [];
        //console.log(results);
        var marker;
        var favorites = results['favorites'];
        // favorites is a dict; need to loop over dict instead of list
        for (var one_favorite in favorites) {
            console.log(one_favorite);
            marker = addMarker(map, favorites[one_favorite]);
            markers.push(marker);
        }
        cb_done(markers);
    });
}

function addMarker(map, one_favorite) {
    var marker = new google.maps.Marker({
        position: one_favorite[0]['location'],
        map: map,
        title: one_favorite[0]['collection']
    });
    attachInfoWindow(map, marker, one_favorite);
    return marker;
}

function attachInfoWindow(map, marker, one_favorite) {

    var contentString = '<div id="content">';
    contentString += '<h3>'+one_favorite[0]['collection']+'</h3>';
    contentString += '<h4><a href='+one_favorite[0]['website']+'>'+one_favorite[0]['website']+'</a></h4>';
    contentString += '<ul>';
    for (var art in one_favorite){
        contentString += '<li class="art"><a href=/artworks/'+one_favorite[art]['art_id']+'>'+one_favorite[art]['title']+'</li>';
    }
    contentString += '</ul></div>';

    var infoWindow = new google.maps.InfoWindow({
        content: contentString
    });

    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });  
}
