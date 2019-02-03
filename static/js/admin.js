jQuery(document).ready(function($) {
	var network = $('#id_network').val();
	var username = $('#id_username').val();
	var key = $('#id_key').val();
	var url = $('#id_url').val();
	var services = $.parseJSON($('#id_service').val());
	// console.log(services);
	$('#id_service').hide();
	// console.log(network);
	if (network != 'undefined' && network != null) {
		$.ajax({
			url: '/get_services/',
			type: 'POST',
			dataType: 'json',
			data: {network: network, username: username, key:key, url: url},
			success: function(data){
				var options = '';
				for(var id in data)
				{
					options += '<option value="'+ id + '"'
					for(var s in services)
					{
						var service = s + ':' + services[s];
						// console.log(service);
						if ( service == id) {
							options += 'selected="selected"'
						}
					}
					options += '>' + data[id] +'</option>';
				}

				$('#id_service').replaceWith('<select id="id_service" name="service" multiple>'+ options +'</select>').show();
			}
		});
		
	}
	else{
		alert('authentication failed/invalid ip');
		// window.history.back();
	}

	$('#id_network').on('change', function(event){
		var network = $(this).val()
		if (network != 'undefined') {
			$.ajax({
				url: '/get_services/',
				type: 'POST',
				dataType: 'json',
				data: {network: network, username: username, key:key, url: url},
				success: function(data){
					// console.log(data);
					var options = '';
					for(var id in data)
					{
						options += '<option value="'+ id +'">'+ data[id] +'</option>';
					}
					// console.log(options);
					$('#id_service').replaceWith('<select id="id_service" name="service" multiple>'+ options +'</select>').show();
				}
			});
			
		}		
	})

});