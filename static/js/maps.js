"use strict";

var map;
function initMap() {
map = new google.maps.Map(document.getElementById('map'), {
  center: {lat: 27.467830, lng: -51.000000},
  // TODO: calc centerpt of all markers
  zoom: 2
}); 

getInfo();
// conssole.log("I'm here");
// var louvreMarker = new google.maps.Marker({
//   position: {lat: 48.860621, lng: 2.337642},
//   map: map
// });
}

function getInfo(){
$.get('/get_info', function(results){
    console.log(results);
    var marker;
    var favorites = results['favorites'];
    for (var one_favorite of favorites){
        marker = addMarker(one_favorite);
    }});
}

function addMarker(one_favorite) {
  var LatLng = new google.maps.LatLng(one_favorite['lat'], one_favorite['lng'])
  var marker = new google.maps.Marker({
      position: LatLng,
      map: map,
      title: one_favorite['title'],
  });
  return marker;
}
