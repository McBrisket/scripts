$(document).ready(function() {
	// Handle click event on Start button
	$('#startButton').click(function() {
		// Gather input values
		var selectedInterface = $('#interface').val();
		var enableGPS = $('#gps').is(':checked');
		var enableBSSIDFilter = $('#bssid').is(':checked');
		var bssidValue = $('#bssidEntry').val().trim();
		var enableESSIDFilter = $('#essid').is(':checked');
		var essidValue = $('#essidEntry').val().trim();
		var enableChannelFilter = $('#channel').is(':checked');
		var channelValue = $('#channelEntry').val().trim();
		var saveSurvey = $('#save').is(':checked');
		var filenameValue = $('#filenameEntry').val().trim();
		
		// Construct the command
		var command = ['airodump-ng', selectedInterface];
		if (enableGPS) {
			command.push('--gpsd');
		}
		if (enableBSSIDFilter && bssidValue) {
			command.push('--bssid', bssidValue);
		}
		if (enableESSIDFilter && essidValue) {
			command.push('--essid', essidValue);
		}
		if (enableChannelFilter && channelValue) {
			command.push('--channel', channelValue);
		}
		if (saveSurvey && filenameValue) {
			command.push('-w', filenameValue);
		}
		
		// Execute the command using fetch and handle the response
		fetch('/start-survey', {
			method: 'POST',
		body: JSON.stringify({ command: command }),
			  headers: { 'Content-Type': 'application/json' }
		})
		.then(function(response) {
			if (response.ok) {
				// Handle a successful response
				console.log('Survey started successfully!');
			} else {
				// Handle an error response
				console.error('Failed to start the survey.');
			}
		})
		.catch(function(error) {
			// Handle a network error
			console.error('Network error:', error);
		});
	});
});
