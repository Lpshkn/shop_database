function logsAjax(logs_table_name, id_field_name, obj_id, fillModalFunction) {
	let xhr, post_url, uri;
	post_url = '/logs'
	xhr = new XMLHttpRequest();

	xhr.open('POST', post_url);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onload = function() {
	    if (xhr.status === 200) {
	        fillModalFunction(JSON.parse(xhr.responseText).logs);
	    }
	    else if (xhr.status !== 200) {
	        console.log("Error on sending post request.");
	    }
	};

	uri = `logs_table_name=${logs_table_name}`;
	uri += `&id_field_name=${id_field_name}`;
	uri += `&obj_id=${obj_id}`;

	xhr.send(encodeURI(uri));
}

function fillLogsModal(logs_table_name, id_field_name, obj_id) {
    const logsDiv = document.getElementById('logs-div');
    logsDiv.innerHTML = '';
    logsAjax(logs_table_name, id_field_name, obj_id, function (logs) {
        for (let i = 0; i < logs.length; i++) {
            const logP = document.createElement('p');
            logP.innerHTML = logs[i];
            logsDiv.appendChild(logP);
        }
        if (logs.length === 0) {
        	logsDiv.innerHTML = 'No changes<br>';
		}
    });
}