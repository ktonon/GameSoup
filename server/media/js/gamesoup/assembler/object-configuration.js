(function() {
gamesoup.namespace('gamesoup.builder');

var gs = gamesoup;
var mod = gamesoup.builder;

mod.ObjectConfiguration = Class.create();
mod.ObjectConfiguration.addMethods(mod.ObjectHighlighter);
mod.ObjectConfiguration.addMethods({
	initialize: function(node) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._removeButton = this._node.down('.remove[type=button]');
		this._parameterButtons = this._node.select('.parameter[type=button]');
		this._ownershipNode = this._node.down('.ownership .value');
		// Other initialization
		this.installHighlighter();
		// Event handlers
		this._removeButton.observe('click', this.requestRemoval.bind(this));
		this._parameterButtons.each(function(button) {
			if (button.hasClassName('built-in')) {
				button.observe('click', this.requestBuiltInParameterSetting.bind(this, button));
			} else {
				button.observe('click', this.requestParameterSetting.bind(this, button));				
			}
		}.bind(this))
		if (this._ownershipNode) {
			// Objects that have state are either owned by the game or the player.
			// This widget allows the designer to toggle ownership of stateful objects.
			this._ownershipNode.observe('click', this.requestToggleOwnership.bind(this));			
		}
	},
	/********************************************************/
	/* QUERIES
	/********************************************************/
	getObjectID: function() {
		return this._objectID;
	},
	/********************************************************/
	/* COMMANDS
	/********************************************************/
	requestRemoval: function() {
		this._node.fire('object:removalRequested');
	},
	requestParameterSetting: function(parameter) {
		parameter.fire('object:parameterSettingRequest');
	},
	requestBuiltInParameterSetting: function(parameter) {
		parameter.fire('object:builtInParameterSettingRequest');
	},
	requestToggleOwnership: function() {
		this._node.fire('object:toggleOwnershipRequest');
	},
	toggleOwnershipDisplay: function() {
		if (this._ownershipNode.innerHTML == 'game') {
			this._ownershipNode.innerHTML = 'player';
		} else {
			this._ownershipNode.innerHTML = 'game';
		}
	}
});
gs.tracerize('ObjectConfiguration', mod.ObjectConfiguration);

    
})();
