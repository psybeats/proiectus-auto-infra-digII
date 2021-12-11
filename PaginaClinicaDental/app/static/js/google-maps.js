function initMap() {
    // Latitude and Longitude
    var myLatLng = {lat: 18.85065293194235, lng:-99.20062217696679};

    var map = new google.maps.Map(document.getElementById('google-maps'), {
        zoom: 17,
        center: myLatLng
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: 'Emiliano Zapata, Mor' // Title Location
    });
}