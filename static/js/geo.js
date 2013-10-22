
var map;
var bounds;

function initialize() {

    var mapOptions = {
        zoom: 14,
        center: new google.maps.LatLng("0", "0"),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    bounds = new google.maps.LatLngBounds();

    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(document.getElementById('legend'));
}

function addMarker(photo) {
    var markerLatLng = new google.maps.LatLng(photo.latitude, photo.longitude);
    var icon = "http://maps.google.com/mapfiles/marker.png";
    if(photo.has_geo) {
        icon = "http://maps.google.com/mapfiles/marker_green.png";
    }
    var marker = new google.maps.Marker({
            position: markerLatLng,
            map: map,
            title: photo.title,
            icon: icon
    });
    bounds.extend(markerLatLng);

    var infoWindow = new google.maps.InfoWindow({
        content: '<img src="'+ photo.url +'" class="img-polaroid pull-left">'
    });
    google.maps.event.addListener(marker, 'mouseover', function() {
        infoWindow.open(map, marker);
    });
    google.maps.event.addListener(marker, 'mouseout', function() {
        infoWindow.close();
    });
}

function show_markers(photos) {
    if (photos) {
        for (i in photos) {
            addMarker(photos[i]);
        }
    }
    map.fitBounds(bounds);
}

function show_points(points) {
    var flightPlanCoordinates = [];

    for(i in points) {
        var point = points[i];
        flightPlanCoordinates[i] = new google.maps.LatLng(point.latitude, point.longitude);
    }
    new google.maps.Polyline({
        path: flightPlanCoordinates,
        map: map,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
}

function show_map(photos, points){
    initialize();
    show_markers(photos);
    show_points(points);
}

function save_coordinates() {

    $.blockUI({ message: '<h4>' + save_coordinates_message + '</h4>' });

    $.ajax({
        url: save_coordinates_url,
        type: "POST",
        data: {
            'csrfmiddlewaretoken': csrftoken
        }
    })
    .done(function(){
        window.location.reload();
    })
    .fail(function(e) {
        $.unblockUI();
        alert('Ups '+ e.statusText);
    });

//
}