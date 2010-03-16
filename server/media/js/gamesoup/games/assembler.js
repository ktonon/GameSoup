(function() {
gamesoup.namespace('gamesoup.games');

var gs = gamesoup;
var mod = gamesoup.games;


gs.gridSize = 20;


mod.Assembler = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._tabset = new gs.layout.TabSet(this._node);
	}
});
gs.tracerize('Assembler', mod.Assembler);


document.observe('dom:loaded', function() {
	gamesoup.games.assembler = new gamesoup.games.Assembler('assembler');
});
})();
