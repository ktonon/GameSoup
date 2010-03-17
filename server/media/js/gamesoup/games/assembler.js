(function() {
gamesoup.namespace('gamesoup.games');

var gs = gamesoup;
var mod = gamesoup.games;


gs.gridSize = 20;


mod.Assembler = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._gameID = this._node.getAttribute('gameID');
		this._options = {gameID: this._gameID};
		this._tabset = new gs.layout.TabSet(this._node);
		this._objects = new mod.ObjectList('object-list', this._options);
		this._canvas = new mod.Canvas('canvas', this._options);
	}
});
gs.tracerize('Assembler', mod.Assembler);


mod.MessageBox = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._valueNode = this._node;
	},
	post: function(message) {
		this._valueNode.innerHTML = message;
	},
	clear: function() {
		this._valueNode.innerHTML = '';
	}
});


document.observe('dom:loaded', function() {
	gamesoup.games.assembler = new gamesoup.games.Assembler('assembler');
	gamesoup.games.messageBox = new gamesoup.games.MessageBox('message-box');
});
})();
