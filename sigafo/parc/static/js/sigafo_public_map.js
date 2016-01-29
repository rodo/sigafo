/*
 * Main map
 *
 * Publics libs used by other website
 *
 *
 *
 */
function map_init_map (map, mapid) {

    var layer = L.geoJson();
    var markers = new L.MarkerClusterGroup();
    var idmap = mapid.toString();
    var dataurl = 'http://sigadev.lafrere.net/map/'+idmap+'/geojsonp?callback=parsejson';
    var url = 'http://sigadev.lafrere.net/map/'+idmap+'/geojsonp';

    //$.getJSON(dataurl, function (data) { });

    $.ajax({
	url: url,

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

            var markurl = "http://www.agforward.eu/files/agforward/css/images/People.png";

            var greenIcon = L.icon({
                iconUrl: markurl,

                iconSize:     [32, 32], // size of the icon
                iconAnchor:   [16, 31], // point of the icon which will correspond to marker's location
                popupAnchor:  [-3, -16] // point from which the popup should open relative to the iconAnchor
            });
  
		    var marker = L.marker(new L.LatLng(parcel.geometry.coordinates[1],
						                       parcel.geometry.coordinates[0]), { title: parcel.properties.title, icon: greenIcon });


            img = '<img src="'+parcel.properties.map_public_info.image+'"/>';

            var popup = img;

            popup = popup + "<h3>"+parcel.properties.name+"</h3>";

            //Stakeholder group: AGFORWARD UK Wood Pasture and Parkland Group

            popup = popup + "<div>Contact : "+parcel.properties.map_public_info.contact+"</div>";
            popup = popup + "<div>E-mail : "+parcel.properties.map_public_info.email+"</div>";
            popup = popup + "<div>Address : "+parcel.properties.map_public_info.town+"</div>";


            popup = popup + '<div>Coordinates: '+ parcel.properties.map_public_info.latitude;
            popup = popup + ', '+ parcel.properties.map_public_info.longitude+'</div>';

            popup = popup + '<div>Website with further details: <a href="'+parcel.properties.map_public_info.url+'">url</a></div>';

            marker.bindPopup(popup);
		    markers.addLayer(marker);
		}
	    })

	    map.addLayer(markers);

	}
    });


}

function map_init_basic (map, options) {
    /* deprecated use map_init_map instead */
    var layer = L.geoJson();
    var markers = new L.MarkerClusterGroup();
    var dataurl = 'http://sigadev.lafrere.net/map/3/geojsonp?callback=parsejson';

    //$.getJSON(dataurl, function (data) { });

    $.ajax({
	url: "http://sigadev.lafrere.net/map/3/geojsonp",

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
