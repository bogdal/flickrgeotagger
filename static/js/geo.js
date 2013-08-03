
function show_map() {

    var mapOptions = {
        zoom: 14,
        center: new google.maps.LatLng("0", "0"),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    var bounds = new google.maps.LatLngBounds();

    map.fitBounds(bounds);
}