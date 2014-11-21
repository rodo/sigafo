/*
 * API
 *
 *
 *
 */
function parcel_list (dataurl) {

    $.getJSON(dataurl, function (data) {
		$('#pager-previous').href = 'toto';
        /* layer.addData(data); */
        // datas = data.results;

        // datas.forEach(function(parcel) {
		// 				var span = Mustache.render(button,
		// 							   {name: item,
		// 							   id: data.result});
		// 				$('#job-tools').append(span);
        // })
    });

    map.addLayer(markers);
}
