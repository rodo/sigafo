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
    var dataurl = 'http://sigadev.lafrere.net/map/1/geojsonp?callback=parsejson';

    //$.getJSON(dataurl, function (data) { });

    $.ajax({
	url: "http://sigadev.lafrere.net/map/1/geojsonp",

    // the name of the callback parameter, as specified by the YQL service
	jsonp: "callback",

    // tell jQuery we're expecting JSONP
	dataType: "jsonp",

    // tell YQL what we want and that we want JSON
	data: {},

    // work with the response
	success: function( response ) {
	    datas = response.features;
    
	    datas.forEach(function(parcel) {
	
		if (parcel.geometry != null ){
		    var marker = L.marker(new L.LatLng(parcel.geometry.coordinates[1],
						       parcel.geometry.coordinates[0]), { title: parcel.properties.title });
                    marker.bindPopup("<h3>"+parcel.properties.title+"</h3><div><b>Description</b></div><div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque id sapien augue. Morbi leo orci, iaculis vehicula mauris sit amet, consectetur convallis orci. Vestibulum vulputate nunc quis nunc vulputate pharetra. Maecenas quis mollis libero, ac molestie leo. Suspendisse malesuada congue nibh. Aenean vel lobortis nunc, in auctor sem. Morbi non risus diam. Cras in augue in lorem lacinia pellentesque non eget ipsum. Ut nec placerat ligula. Vestibulum sit amet mauris ex. Cras imperdiet ullamcorper sapien id congue. Nunc fringilla varius rutrum.</div>");
		    markers.addLayer(marker);
		}
	    })
	    
	    map.addLayer(markers);

	}
    });


}

function parsejson (data) {

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
                marker.bindPopup("<h2>"+parcel.properties.title+"</h2>");
                markers.addLayer(marker);
            }
        })
    });

    map.addLayer(markers);
}
