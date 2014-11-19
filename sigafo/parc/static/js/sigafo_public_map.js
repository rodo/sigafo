/*
 * Main map
 *
 * Publics libs used by other website
 *
 *
 *
 */
function map_init_basic (map, options) {

    var layer = L.geoJson();
    var markers = new L.MarkerClusterGroup();

    var dataurl = '/parcel/geojson';

    $.getJSON(dataurl, function (data) {
        /* layer.addData(data); */
        datas = data.features;

        datas.forEach(function(parcel) {

            if (parcel.geometry != null ){
                var marker = L.marker(new L.LatLng(parcel.geometry.coordinates[1],
                                                   parcel.geometry.coordinates[0]), { title: parcel.properties.title });
                marker.bindPopup(parcel.properties.title);
                markers.addLayer(marker);
            }
        })

    });

    map.addLayer(markers);
}
//
function map_init_data (map, options, mapurl, dataurl) {

    var layer = L.geoJson();
    var markers = new L.MarkerClusterGroup();

    $.getJSON(mapurl, function (data) {
        map.panTo([data.center_lat, data.center_lon]);
    });

    $.getJSON(dataurl, function (data) {
        /* layer.addData(data); */
        datas = data.features;

        datas.forEach(function(parcel) {

            if (parcel.geometry != null ){
                var marker = L.marker(new L.LatLng(parcel.geometry.coordinates[1],
                                                   parcel.geometry.coordinates[0]), { title: parcel.properties.title });
                marker.bindPopup(parcel.properties.title);
                markers.addLayer(marker);
            }
        })
    });

    map.addLayer(markers);
}
