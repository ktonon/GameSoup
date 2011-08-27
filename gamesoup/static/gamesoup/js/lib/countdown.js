var request;
var callback = new function() {
	this.weddingDate = "";
	this.success = function (o) {
		this.showCountDown(o.responseText);
	}
	this.failure = function (o) {
		this.showCountDown(get_countdown(this.weddingDate));
	}
	this.showCountDown = function (days) {
		if (days != 0) {
			document.getElementById('c-countdown-days').appendChild(document.createTextNode(Math.abs(days)));
		}
		document.getElementById('c-countdown-text').appendChild(document.createTextNode(get_countdown_string(days)));
		document.getElementById('c-countdown').style.display = 'block';
	}
}

function display_countdown(wedding_date) {
	callback.weddingDate = wedding_date;
	request = YAHOO.util.Connect.asyncRequest('GET', '/apps/public/mysite/countdown.php?date=' + escape(wedding_date), callback);
}

function get_countdown(wedding_date) {
	var then = new Date(wedding_date);
	var now = new Date;	
	var diff = then.valueOf() - now.valueOf();
	return Math.ceil(diff / 1000 / 60 / 60 / 24);
}
	
function get_countdown_string(days) {	
	if (days == 0) return 'Today is our wedding!';
	else if (days == -1) return ' day since our wedding!';
	else if (days < 0) return ' days since our wedding!';	
	else if (days == 1) return ' day until our wedding!';
	else return ' days until our wedding!';
}