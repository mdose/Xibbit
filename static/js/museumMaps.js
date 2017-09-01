"use strict";

function initMap() {
    var mapData = $('#map_data').data();
    var map = new google.maps.Map(document.getElementById('map'), {
        center: mapData,
        zoom: 13
    });

    var mapTitle = $('#map_title').data('title');
    var marker = new google.maps.Marker({
        position: mapData,
        map: map,
        title: mapTitle,
    });

}