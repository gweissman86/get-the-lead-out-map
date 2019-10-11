
function loadText(url, callback) {
	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	xobj.open("GET", url, true);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == 200) {
			callback(xobj.responseText);
		}
	}
	xobj.send(null);
}

function loadTSV(url, callback) {
	loadText(url + '.tsv', function(text){
		const lines = text.split("\n").slice(1, -1);
		const rows = lines.map(function(line) {
			return line.split("\t");
		});
		callback(rows);
    });
}

function loadCSVFromText(text, callback) {
	const splat = text.split("\n");
	const header = splat[0].split(",");
	const lines = splat.slice(1, -1);
	const rows = lines.map(function(line) {
		const row = {};
		line.split(",").forEach(function(cellValue, index) {
			row[header[index]] = cellValue;
		});
		return row;
	});
	callback(rows);
}

function getById(id) {
	return document.getElementById(id);
}

function getValue(id) {
	return getById(id).value;
}

function setValue(id, value) {
	getById(id).value = value;
}

function hideById(id) {
	getById(id).style.display = "none";
}

function showById(id) {
	getById(id).style.display = "block";
}

function setStateById(id, key, value) {
	getById(id).setAttribute(key, value);
}

function removeClass(id, className) {
	var tag = getById(id);
	tag.className = tag.className.replace(className, "").trim();
}

function addClass(id, className) {
	var tag = getById(id);
	tag.className = (tag.className.replace(className, "") + " " + className).trim();
}

function serializeXmlNode(xmlNode) {
	if (typeof window.XMLSerializer != "undefined") {
		return (new window.XMLSerializer()).serializeToString(xmlNode);
	} else if (typeof xmlNode.xml != "undefined") {
		return xmlNode.xml;
	}
	return "";
}

function toNumber(inpt) {
	try {
		return Number(inpt);
	} catch (error) {
		return inpt;
	}
}
  