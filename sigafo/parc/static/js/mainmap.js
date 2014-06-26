/*
 * Main map
 * 
 * 
 * 
 */
function map_move(lon, lat) {
    map.panTo([lat, lon]);
}
/*
*
*
*/
function map_init_basic (map, options) {
    
    var layer = L.geoJson();
    var markers = new L.MarkerClusterGroup();

    $.getJSON("/parcel/geojson", function (data) {
        /* layer.addData(data); */
        datas = data.features;
        
        datas.forEach(function(parcel) {
            var title = "title";
            if (parcel.geometry != null ){
                var marker = L.marker(new L.LatLng(parcel.geometry.coordinates[1],
                                                   parcel.geometry.coordinates[0]), { title: title });
                marker.bindPopup(title);
                markers.addLayer(marker);
            }
        })
        
    });


    map.addLayer(markers);
}