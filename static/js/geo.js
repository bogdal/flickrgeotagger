
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

function chunk (arr, len) {

  var chunks = [],
      i = 0,
      n = arr.length;

  while (i < n) {
    chunks.push(arr.slice(i, i += len));
  }

  return chunks;
}

function init_message_popup(total) {
    $("#message_popup .total").html(total);
    $("#message_popup .counter").html(0);
}

function increase_popup_counter(items) {
    var counter = $("#message_popup .counter");
    var value = parseInt(counter.html()) + items;
    counter.html(value);
}

function save_chunk(index, chunks) {
    var chunk = chunks[index];

    if(chunk != undefined) {
        $.ajax({
            url: save_coordinates_url,
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'photos': JSON.stringify(chunk)
            }
        })
        .done(function(){
            increase_popup_counter(chunk.length);
            save_chunk(++index, chunks);
        })
        .fail(function(e) {
            $.unblockUI();
            alert('Ups '+ e.statusText);
        });
    } else {
        window.location.reload();
    }
}

function save_coordinates(photos) {

    $.blockUI({ message: $("#message_popup") });

    init_message_popup(photos.length);
    save_chunk(0, chunk(photos, 10));
}