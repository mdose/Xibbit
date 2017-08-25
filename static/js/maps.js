"use strict";

  var map;
  function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 27.467830, lng: -51.000000},
      zoom: 2
    });
    // console.log("I'm here");
  }