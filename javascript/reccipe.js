/*
source: http://stackoverflow.com/questions/14446447/javascript-read-local-text-file
credit: http://stackoverflow.com/users/971904/danny
*/


Element.prototype.add_text = function (txt) {
	this.appendChild(
		document.createTextNode(txt)
	)
	return this;
};

Element.prototype.grow = function (tag, attribute_map) {
	var child = document.createElement(tag);
	if ( typeof(attribute_map) !== 'undefined' ) {
		for (let key in attribute_map) {
			child.setAttribute(key, attribute_map[key]);
		}
	}
	this.appendChild(child);
	return child;
};

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
};

String.prototype.format = function() {
	var args = arguments;
	return this.replace(/{(\d+)}/g, function(match, number) { 
		return typeof args[number] != 'undefined' ? args[number] : match;
	});
};


Element.prototype.clear = function () {
	while (this.firstChild) {
		this.removeChild(this.firstChild);
	}
	return this;
};


/*
function getTextFile(file) {
	// return the content of a local or remote text file
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", file);
	rawFile.onreadystatechange = function () {
		if(rawFile.readyState === 4) {
			if(rawFile.status === 200 || rawFile.status == 0) {
				return rawFile.responseText;
			}
		}
	}
	rawFile.send(null);
}

// readTextFile("file:///C:/your/path/to/file.txt");


// http://stackoverflow.com/questions/7346563/loading-local-json-file
function loadJSON(url, callback) {   

	var obj = new XMLHttpRequest();
	obj.overrideMimeType("application/json");
	obj.open('GET', url,  true);
	obj.onreadystatechange = function () {
		if(rawFile.readyState === 4) {
			if(rawFile.status === 200 || rawFile.status == 0) {
				callback(JSON.parse(obj.responseText));
			}
		}
	};
	obj.send(null);  
}
*/