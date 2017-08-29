"use strict";

var map;
var markers = [];
// var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
function initMap() {
map = new google.maps.Map(document.getElementById('map'), {
  center: {lat: 54.5260, lng: 15.2551},
  // Europe Coordinates ^
  // center: {lat: 27.467830, lng: -51.000000},
  // World Coordinates; zoom: 2
  // TODO: calc centerpt of all markers
  zoom: 4
}); 


doAll();
console.log(markers);



// var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
// conssole.log("I'm here");
// var louvreMarker = new google.maps.Marker({
//   position: {lat: 48.860621, lng: 2.337642},
//   map: map
// });
// var markers = getInfo();
//           return new google.maps.Marker({
//             position: LatLng,
//             label: labels[i % labels.length]
//           });
//         });
        

        // Add a marker clusterer to manage the markers.
// var markerCluster = new MarkerClusterer(map, markers,
//     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}


function getInfo(_callback){
$.get('/get_info', function(results){
    console.log(results);
    var marker;
    var favorites = results['favorites'];
    for (var one_favorite of favorites){
        marker = addMarker(one_favorite);
        markers.push(marker);
    }
    _callback();
});
}

function addMarker(one_favorite) {
  var LatLng = new google.maps.LatLng(one_favorite['lat'], one_favorite['lng'])
  var marker = new google.maps.Marker({
      position: LatLng,
      map: map,
      title: one_favorite['title']
   });
  return marker;
}

function doAll(){
 getInfo(function() { 
    var markerCluster = new MarkerClusterer(map, markers,
    {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
});
}

// function addInfoWindow() {

//   var contentString = '<div id="content">' +
//     '<h1>Test</h1>' +
//     '</div>';

//   var infoWindow = new google.maps.InfoWindow({
//     content: contentString,
//     maxWidth: 200
//   });

//   var marker = ?

//   marker.addListener('click', function() {
//   infoWindow.open(map, marker);
//   });  
// }

