const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
const port = 3000;

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.post('/start-survey', (req, res) => {
	const { command } = req.body;
	
	// Randomize MAC address
	const macCommand = `sudo ifconfig ${command.interface} down && sudo macchanger -rb ${command.interface} && sudo ifconfig ${command.interface} up`;
	
	exec(macCommand, (error) => {
		if (error) {
			console.error(`Error randomizing MAC address: ${error}`);
			res.status(500).send('Failed to start the survey');
		} else {
			// Put card into monitor mode
			const monitorModeCommand = `sudo airmon-ng start ${command.interface}`;
			
			exec(monitorModeCommand, (error) => {
				if (error) {
					console.error(`Error enabling monitor mode: ${error}`);
					res.status(500).send('Failed to start the survey');
				} else {
					// Run airodump command
					const airodumpCommand = `airodump-ng ${command.interface} ${buildAirodumpFilter(command)}`;
					
					exec(airodumpCommand, (error, stdout) => {
						if (error) {
							console.error(`Error running airodump: ${error}`);
							res.status(500).send('Failed to start the survey');
						} else {
							res.send(stdout);
						}
					});
				}
			});
		}
	});
});

function buildAirodumpFilter(command) {
	let filter = '';
	
	if (command.enableGPS) {
		filter += '--gpsd ';
	}
	
	if (command.enableBSSIDFilter && command.bssid) {
		filter += `--bssid ${command.bssid} `;
	}
	
	if (command.enableESSIDFilter && command.essid) {
		filter += `--essid ${command.essid} `;
	}
	
	if (command.enableChannelFilter && command.channel) {
		filter += `--channel ${command.channel} `;
	}
	
	if (command.saveSurvey && command.filename) {
		filter += `-w ${command.filename} `;
	}
	
	return filter;
}

app.listen(port, () => {
	console.log(`Server listening on port ${port}`);
});
