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
	release: function() {
		this._objects.invoke('release');
	},
	addObject: function(node) {
		return new mod.Object(node, this._options);
	}
});
gs.tracerize('ObjectList', mod.ObjectList);


mod.Object = Class.create();
mod.Object.addMethods({
	initialize: function(node, options) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._options = {objectID: this._objectID};
		Object.extend(this._options, options);
		this._node.setAttribute('configURL', gs.utils.makeURL('objectConfigureDialog', this._options));
		this._node.setAttribute('deleteURL', gs.utils.makeURL('deleteObject', this._options));
		this._typeButton = this._node.down('.type input[type=button]');
		this._deleteButton = this._node.down('.delete-link');
		// Event handlers
		this._typeButton.observe('click', function() {this._node.fire('object:requestConfig')}.bind(this));
		this._deleteButton.observe('click', function() {this._node.fire('object:requestDeletion')}.bind(this));
	},
	release: function() {
		this._typeButton.stopObserving('click');
		this._deleteButton.stopObserving('click');
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
