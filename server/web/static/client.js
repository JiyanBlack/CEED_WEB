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

    mydom['submit'].addEventListener('click', function (event) {
        event.preventDefault();
        var cardId = mydom['card-id'].value;

        var httpRequest;
        // Old compatibility code, no longer needed.
        if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
            httpRequest = new XMLHttpRequest();
        } else if (window.ActiveXObject) { // IE 6 and older
            httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
        }
        console.log(cardId, httpRequest);

        httpRequest.onreadystatechange = dealResponse;

        httpRequest.open('GET', 'cardid/' + cardId.toString());
        httpRequest.send();

        function dealResponse() {
            // process the server response
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                // everything is good, the response is received
                if (httpRequest.status === 200) {
                    // perfect!
                    var script = document.createElement('script');
                    window.response_routes_json = JSON.parse(httpRequest.responseText);
                    script.text = 'for(var counter=0;counter<response_routes_json.length;counter++){renderSingleJso' +
                            'n(response_routes_json[counter], counter+1)}';
                    document
                        .getElementsByTagName('head')[0]
                        .appendChild(script);
                } else {
                    alert('Server Response With Status Code: ' + httpRequest.status.toString());
                }
            }
        }

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

    //random return a hex color
    function randomPickColor() {
        //specify that no hex value can be greater than 7
        function generate_one_hex_value() {
            var shallowBound = 9;
            return Math.floor(Math.random() * shallowBound).toString()
        }
        var cur_color = "";
        for (var i = 0; i < 6; i++) {
            cur_color += generate_one_hex_value();
        }
        return cur_color;
    }

    //draw polyline
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

    function isIn(obj, array) {
        for (var i = 0; i < array.length; i++) {
            if (array[i] === obj) 
                return true;
            }
        return false;
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
    ajson = JSON.parse(ajson);
    var start_address = ajson.departure_stop.name;
    var start_latlon = ajson.departure_stop.location;
    var end_address = ajson.arrival_stop.name;
    var end_latlon = ajson.arrival_stop.location;
    // find all bus number without duplicates
    var cur_line;
    var all_bus_number = [];
    for (var i = 0; i < ajson.routes.length; i++) {
        cur_line = ajson.routes[i];
        all_bus_number.push(cur_line.name);
        drawLineByEncoded(cur_line.polyline.points, randomPickColor());
    }
    var final_bus_number = [];
    for (var i = 0; i < all_bus_number.length; i++) {
        if (!isIn(all_bus_number[i], final_bus_number)) {
            final_bus_number.push(all_bus_number[i]);
        }
    }

    var start_label = '<div>' + start_address + '</div><div>' + final_bus_number.join('|') + '</div><div>Latitude: ' + start_latlon.lat + ', Longitude: ' + start_latlon.lng + '</div>';
    var end_label = '<div>' + end_address + '</div><div>' + final_bus_number.join('|') + '</div><div>Latitude: ' + end_latlon.lat + ', Longitude: ' + end_latlon.lng + '</div>';
    addMarker(start_label, "", start_latlon.lat, start_latlon.lng);
    addMarker(end_label, "", end_latlon.lat, end_latlon.lng);

}

startRun();