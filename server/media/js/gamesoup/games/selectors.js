(function() {
gamesoup.namespace('gamesoup.games.selectors');

var gs = gamesoup;
var mod = gamesoup.games.selectors;

mod.SingleObjectSelector = Class.create({
	initialize: function(objects, callback) {
		$('scratch').show()
		this._scratch = $('scratch').down('.inner-container');
		this._scratch.fire('selector:started');
		// Setup the callback
		this._callback = callback;
		// Setup the selector buttons
		this._objects = objects;
		this._selectors = this._objects.collect(this.addSelector.bind(this));
		this._watchCancel = this.cancel.bind(this);
		document.observe('keydown', this._watchCancel);
	},
	release: function() {
		this._selectors.invoke('stopObserving', 'click');
        document.stopObserving('keydown', this._watchCancel);
		this._scratch.innerHTML = '';
	    $('scratch').hide();
	    this._scratch.fire('selector:completed');
	},
	/*
	 * For each object, create a button on the scratch space.
	 * When a button is clicked, the selector completes
	 */
	addSelector: function(node) {
		var original = node.down('.type input[type=button]');
		var selector = new Element('input', {
			objectID: node.getAttribute('objectID'),
			type: 'button', 
			value: original.getAttribute('value'), 
			style: 'text-align: left; font-weight: bold; position: absolute'
		});
		this._scratch.insert({bottom: selector});
		selector.clonePosition(original, {
			offsetTop: -2,
			offsetLeft: 1
		});
		// Event handlers
		selector.observe('click', this.selectAndRelease.bind(this));
		return selector;
	},
	selectAndRelease: function(event) {
		var objectID = event.target.getAttribute('objectID');
		this._callback(objectID);
		this.release();
	},
	cancel: function(event) {
	    if (event.keyCode == Event.KEY_ESC) {
	        event.stop();
	        gs.games.messageBox.clear();
	        this.release();
	    }
	}
});
gs.tracerize('SingleObjectSelector', mod.SingleObjectSelector);


mod.MultipleObjectSelector = Class.create({
	initialize: function(objects, callback) {
		$('curtain').show();
		$('scratch').show()
		this._scratch = $('scratch').down('.inner-container');
		this._scratch.fire('selector:started');
		// Setup the callback
		this._callback = callback;
		// Create the selector buttons
		this._objects = objects;
		this._selectors = this._objects.collect(this.addSelector.bind(this));
		this._doneButton = new Element('input', {
			type: 'button',
			value: 'Search',
			style: 'position: fixed; top: 190px; left: 230px; font-size: 18pt; padding: 100px'
		});
		this._scratch.insert({bottom: this._doneButton});
		this._doneButton.observe('click', this.selectAndRelease.bind(this));
		this._watchCancel = this.cancel.bind(this);
		document.observe('keydown', this._watchCancel);
	},
	release: function(event) {
		this._doneButton.stopObserving();
		this._selectors.invoke('stopObserving', 'click');
		this._scratch.innerHTML = '';
		$('curtain').hide();
		$('scratch').hide()
        document.stopObserving('keydown', this._watchCancel);
		this._scratch.fire('selector:completed');
	},
	/*
	 * For each object, create a button on the scratch space.
	 * When a button is clicked it toggles on and off.
	 */
	addSelector: function(node) {
		var original = node.down('.type input[type=button]');
		var selector = new Element('input', {
			objectID: node.getAttribute('objectID'),
			type: 'button', 
			value: original.getAttribute('value'), 
			style: 'text-align: left; font-weight: bold; position: absolute'
		});
		this._scratch.insert({bottom: selector});
		selector.clonePosition(original, {
			offsetTop: -2,
			offsetLeft: 1
		});
		// Event handlers
		selector.observe('click', this.toggleSelector.bind(this));
		return selector;
	},
	toggleSelector: function(event) {
		var node = event.target;
		var action = node.hasClassName('selected') ? 'remove' : 'add';
		node[action + 'ClassName']('selected');
	},
	selectAndRelease: function(event) {
	    var objectIDs = this._selectors.collect(function(node) {
			if (node.hasClassName('selected')) return node.getAttribute('objectID');
		}).filter(function(x) {return x});
		this._callback(objectIDs);
		this.release();
	},
	cancel: function(event) {
	    if (event.keyCode == Event.KEY_ESC) {
	        event.stop();
	        gs.games.messageBox.clear();
	        this.release();
	    }
	}
});
gs.tracerize('MultipleObjectSelector', mod.MultipleObjectSelector);
    
})();
