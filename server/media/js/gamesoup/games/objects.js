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
		this._boundRefs = this._node.select('.parameter.bound.reference');
		this._ownershipNode = this._node.down('.ownership.stateful');
		// Event handlers
		this._typeButton.observe('click', function() {this._node.fire('object:requestConfig')}.bind(this));
		this._deleteButton.observe('click', function() {this._node.fire('object:requestDeletion')}.bind(this));
		if (this._ownershipNode) this._ownershipNode.observe('click', this.toggleOwnership.bind(this));
		// Highlighting
		this._boundRefs.each(function(node) {
		    var boundToID = node.getAttribute('boundTo');
		    var boundToNode = $('object-' + boundToID)
            node.observe('mouseover', function(otherNode, event) {otherNode.addClassName('highlight');}.curry(boundToNode));
            node.observe('mouseout', function(otherNode, event) {otherNode.removeClassName('highlight');}.curry(boundToNode));		        
	    }.bind(this));
	    this._node.observe('mouseover', this.showShaper.bind(this, 'add'));
	    this._node.observe('mouseout', this.showShaper.bind(this, 'remove'));
	},
	release: function() {
	    this._node.stopObserving('mouseover');
	    this._node.stopObserving('mouseout');
		this._typeButton.stopObserving('click');
		this._deleteButton.stopObserving('click');
		if (this._ownershipNode) this._ownershipNode.stopObserving('click');
		this._boundRefs.invoke('stopObserving');
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
	showShaper: function(action) {
	    var shaper = $('object-shaper-' + this._objectID);
	    if (shaper) shaper[action + 'ClassName']('highlight');
	},
	toggleOwnership: function() {
	    var url = gs.utils.makeURL('toggleObjectOwnership', this._options);
	    new Ajax.Request(url, {
	        method: 'post',
	        evalJS: true,
	        onSuccess: function(transport) {this._node.fire('assembler:systemChanged')}.bind(this)
	    })
	}
});
gs.tracerize('Object', mod.Object);

    
})();
