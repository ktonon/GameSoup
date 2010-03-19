(function() {
gamesoup.namespace('gamesoup.games.dialogHandlers');

var gs = gamesoup;
var mod = gamesoup.games.dialogHandlers;

mod.ConfigureObject = Class.create({
	initialize: function(node, options) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._options = {objectID: this._objectID};
		Object.extend(this._options, options);
		this._builtIns = this._node.select('.built-in').collect(this.addBuiltIn.bind(this));
		this._refs = this._node.select('.ref').collect(this.addRef.bind(this));
		this._doneButton = this._node.down('.submit-row input[type=button]');		
		// Event handlers
		this._doneButton.observe('click', function() {this._node.fire('dialog:requestClose')}.bind(this));
		this._node.observe('parameter:saved', function() {this._node.fire('dialog:systemChanged')}.bind(this));
	},
	release: function() {
		this._builtIns.invoke('release');
		this._doneButton.stopObserving();
		this._node.stopObserving();
	},
	addBuiltIn: function(node) {
		var ParamClass = gamesoup.games.parameters[node.getAttribute('interface')];
		return new ParamClass(node, this._options);
	},
	addRef: function(node) {
	    var RefClass = gamesoup.games.parameters[node.hasClassName('unsatisfiable') ? 'UnsatisfiableReference' : 'Reference'];
		return new RefClass(node, this._options);
	}
})
gs.tracerize('ConfigureObject', mod.ConfigureObject);


})();
