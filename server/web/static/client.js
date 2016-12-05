'use strict';

var mydom = {
    'from-date': document.getElementById('from-date'),
    'to-date': document.getElementById('to-date'),
    'submit': document.getElementById('submit'),
    'reset': document.getElementById('reset'),
    'card-id': document.getElementById('card-id')
}

function startRun() {
    //initialize values...
    function setDateDefault() {
        mydom['from-date'].valueAsDate = new Date(2009, 2, 1);
        mydom['to-date'].valueAsDate = new Date(2009, 2, 1);
    }

    mydom['reset']
        .addEventListener('click', function (event) {
            // event.preventDefault(); setDateDefault(); mydom['card-id'].value = "";

        });
    setDateDefault();
}

function ajax_get(url, callback) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callback(this);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

function initMap() {
    // Create a map object and specify the DOM element for display.

    var map_option = {
        center: {
            lat: -31.986,
            lng: 115.971
        },
        scrollwheel: true,
        zoom: 11,
        mapTypeId: 'roadmap'
    }
    var map = new google
        .maps
        .Map(document.getElementById('map'), map_option);

    window.map = map
    //

    mydom['submit'].addEventListener('click', function (event) {
        event.preventDefault();
        var cardId = mydom['card-id'].value;
        // ajax_get('user/' + cardId, function (xhttp) {
        // console.log(xhttp.responseText); Create a <script> tag and set the USGS URL
        // as the source.
        var script = document.createElement('script');
        // This example uses a local copy of the GeoJSON stored at
        // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
        script.text = 'for(var counter=0;counter<sample.length;counter++){renderSingleJson(sample[count' +
                'er], counter+1)}';
        document
            .getElementsByTagName('head')[0]
            .appendChild(script);
    });
    // });
}

// Loop through the results array and place a marker for each set of
// coordinates. window.displayDataCallback = function(results) { for (var i = 0;
// i < results.features.length; i++) {     var coords =
// results.features[i].geometry.coordinates;     var latLng = new
// google.maps.LatLng(coords[1],coords[0]);     var marker = new
// google.maps.Marker({     position: latLng,     map: map     }); } }

function renderSingleJson(ajson, counter) {

    function randomPickColor() {
        var hexColor = [
            "#ffc0cb",
            "#900090",
            "#051152",
            "#ad5a7a",
            "#f9c780",
            "#5a7aad",
            "#403f51",
            "#e3780a",
            "#00ad06",
            "#461499",
            "#418a14",
            "#794044",
            "#c8ebd0"
        ];
        return hexColor[Math.floor(Math.random() * hexColor.length)];
    }

    function drawLineByEncoded(encoded, color) {
        var decodedPath = google
            .maps
            .geometry
            .encoding
            .decodePath(encoded)
        var apolyline = new google
            .maps
            .Polyline({path: decodedPath, geodesic: true, strokeColor: color, strokeOpacity: 1.0, strokeWeight: 3});
        apolyline.setMap(map);
    }

    // add marker to map
    function addMarker(content, label, lat, lon) {
        var myLatlng = new google
            .maps
            .LatLng(lat, lon);
        var infowindow = new google
            .maps
            .InfoWindow({content: content});
        var marker = new google
            .maps
            .Marker({position: myLatlng, label: label});
        marker.setMap(map);
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });

    }

    var routes = ajson.routes;
    var origin_start,
        origin_end;
    var bus_number = [];
    var start_latlon,
        end_latlon;
    var start_address,
        end_address;
    var target_line;
    //delete routes with two transit in legs
    for (var i = 0; i < routes.length; i++) {
        var cur_route = routes[i];
        var cur_legs = cur_route.legs;
        var transit_number = 0;
        var final_legs;
        var final_steps;
        for (var j = 0; j < cur_legs.length; j++) {
            var cur_steps = cur_legs[j].steps;
            for (var m = 0; m < cur_steps.length; m++) {
                if (cur_steps[m]["travel_mode"] == "TRANSIT") {
                    transit_number += 1;
                    final_legs = cur_legs[j];
                    final_steps = cur_steps[m];
                }
            }
        }
        if (transit_number == 1) {
            final_legs.steps = final_steps;
            routes[i].legs = final_legs;
        } else {
            routes[i] = undefined;
        }
    }
    // console.log(JSON.stringify(routes, null, 2)); find out correct routes,filter
    // out routes with legs that are not same with the first one
    for (var i = 0; i < routes.length; i++) {
        cur_route = routes[i];
        cur_steps = cur_route.legs.steps;
        if (i == 0) {
            start_address = cur_route.legs['start_address'];
            end_address = cur_route.legs['end_address'];
            start_latlon = cur_steps['start_location'];
            end_latlon = cur_steps['end_location'];
            bus_number.push(cur_steps['transit_details']['line']['short_name']);
            target_line = cur_steps.polyline.points;
        } else {
            if (cur_route.legs['start_address'] == start_address && cur_route.legs['end_address'] == end_address) {
                bus_number.push(cur_steps['transit_details']['line']['short_name']);
            }
        }
    }
    drawLineByEncoded(target_line, randomPickColor());
    console.log(bus_number);
    for (var i = 0; i < bus_number.length; i++) {}
    var start_label = '<div>' + start_address + '</div><div>' + bus_number.join('|') + '</div><div>Latitude: ' + start_latlon.lat + ', Longitude: ' + start_latlon.lng + '</div>';
    var end_label = '<div>' + end_address + '</div><div>' + bus_number.join('|') + '</div><div>Latitude: ' + end_latlon.lat + ', Longitude: ' + end_latlon.lng + '</div>';
    addMarker(start_label, counter.toString() + 'S', start_latlon.lat, start_latlon.lng);
    addMarker(end_label, counter.toString() + 'E', end_latlon.lat, end_latlon.lng);
}

startRun();