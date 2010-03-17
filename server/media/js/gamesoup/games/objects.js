(function() {
gamesoup.namespace('gamesoup.games');

var gs = gamesoup;
var mod = gamesoup.games;


mod.ObjectList = Class.create();
mod.ObjectList.addMethods({
	initialize: function(node, options) {
		this._node = $(node);
		this._options = options;
		this._objects = this._node.select('.object').collect(this.addObject.bind(this));
	},
	addObject: function(node) {
		return new mod.Object(node, this._options);
	}
});
gs.tracerize('ObjectList', mod.ObjectList);


mod.Object = Class.create();
// mod.Object.addMethods(mod.ObjectHighlighter);
mod.Object.addMethods({
	initialize: function(node, options) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._options = {objectID: this._objectID};
		Object.extend(this._options, options);
		// this.installHighlighter();
		// Event handlers
	},
	/********************************************************/
	/* QUERIES
	/********************************************************/
	getObjectID: function() {
		return this._objectID;
	}
	/********************************************************/
	/* COMMANDS
	/********************************************************/
});
gs.tracerize('Object', mod.Object);

    
})();
