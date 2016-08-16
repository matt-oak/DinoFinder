//Dino_Map.js
//Plot points of dinosaur findings on Google Map
//Author: Matt Oakley
//Date: 08/15/2016

var count = 0;
var map;
var marker_array = [];
var selected_dinos = [];

function get_selection() {
    count++;
    var selected_dinosaur;
    var x = document.getElementById("dino_list").selectedIndex;
    var y = document.getElementById("dino_list").options;
    selected_dinosaur = y[x].text;
    selected_dinos.push(selected_dinosaur);

    if (count > 1 && selected_dinosaur != selected_dinos[count - 2]){
      clearOverlays();
    }

    var request = new XMLHttpRequest();
	  request.open("GET", "http://localhost:8080/dino/dinosaur_locs/" + selected_dinosaur + ".txt", true);
    request.onload = function() {
  		if (request.status >= 200 && request.status < 400) {
    		var resp = request.responseText;
        var lines = resp.split('\n');
        var entry;
        var index_of_comma;
        var index_of_oparen;
        var index_of_cparen;
        var lat;
        var lon;
        for(var i = 0; i < lines.length - 1; i++){
          entry = lines[i];
          index_of_comma = entry.indexOf(",");
          index_of_oparen = entry.indexOf("(");
          index_of_cparen = entry.indexOf(")");
          lat = entry.slice(index_of_oparen + 1, index_of_comma);
          lon = entry.slice(index_of_comma + 2, index_of_cparen);
          set_point(lat, lon);
        }
  		} 
      else {
        console.log("Unable to load text file");
  		}
	};

	request.onerror = function() {
  		console.log("Unable to load text file");
	};
	request.send();
}

function clearOverlays() {
  for (var i = 0; i < marker_array.length; i++ ) {
    marker_array[i].setMap(null);
  }
  marker_array.length = 0;
}

function set_point(lat, lon){
  var latlon = new google.maps.LatLng(lat, lon);
  var marker = new google.maps.Marker({
    position: latlon,
    animation: google.maps.Animation.DROP,
    map: map
  });
  marker_array.push(marker);
}

function initMap(){
	map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 10, lng: 9.5375},
		zoom: 3
	})
}