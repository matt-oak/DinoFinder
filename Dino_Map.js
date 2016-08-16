//Dino_Map.js
//Plot points of dinosaur findings on Google Map
//Author: Matt Oakley
//Date: 08/15/2016

var selected_dinosaur;
var map;
var lats = [];
var lons = [];

function get_selection() {
    var x = document.getElementById("dino_list").selectedIndex;
    var y = document.getElementById("dino_list").options;
    selected_dinosaur = y[x].text;

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
        for(var line = 0; line < lines.length - 1; line++){
          entry = lines[line];
          index_of_comma = entry.indexOf(",");
          index_of_oparen = entry.indexOf("(");
          index_of_cparen = entry.indexOf(")");
          lat = entry.slice(index_of_oparen + 1, index_of_comma);
          lon = entry.slice(index_of_comma + 2, index_of_cparen);
          lats.push(lat);
          lons.push(lon);
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
  document.getElementById("asdf").click();
  set_points();
}

function set_points(){
  amount_of_coords = lats.length;
  for (var i = 0; i < amount_of_coords; i++){
    var latlon = new google.maps.LatLng(lats[i], lons[i]);
    var marker = new google.maps.Marker({
      position: latlon,
      animation: google.maps.Animation.DROP,
      map: map
    });
  }
}

function initMap(){
	map = new google.maps.Map(document.getElementById("map"), {
		center: {lat: 10, lng: 9.5375},
		zoom: 3
	})
}