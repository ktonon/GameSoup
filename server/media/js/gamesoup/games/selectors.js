(function() {
gamesoup.namespace('gamesoup.games.selectors');

var gs = gamesoup;
var mod = gamesoup.games.selectors;

mod.SingleObjectSelector = Class.create({
	initialize: function(objects) {
		$('scratch').show()
		this._scratch = $('scratch').down('.inner-container');
		this._objects = objects;
		this._selectors = this._objects.collect(this.addSelector.bind(this));
	},
	selectAndRelease: function(event) {
		var selector = event.target;
		this._selectedObjectID = selector.getAttribute('objectID');
		this._selectors.invoke('stopObserving', 'click');
		this._scratch.innerHTML = '';
		this._scratch.fire('selector:released');
		$('scratch').hide();
	},
	getSelectedObjectID: function() {
		return this._selectedObjectID;
	},
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
	}
});
gs.tracerize('SingleObjectSelector', mod.SingleObjectSelector);


mod.MultipleObjectSelector = Class.create({
	initialize: function(objects) {
		$('scratch').show()
		this._scratch = $('scratch').down('.inner-container');
		this._objects = objects;
		this._selectors = this._objects.collect(this.addSelector.bind(this));
		this._doneButton = new Element('input', {
			type: 'button',
			value: 'Search',
			style: 'position: fixed; top: 190px; left: 230px; font-size: 18pt; padding: 100px'
		});
		this._scratch.insert({bottom: this._doneButton});
		this._doneButton.observe('click', this.release.bind(this));
	},
	release: function(event) {
		this._doneButton.stopObserving();
		this._selectors.invoke('stopObserving', 'click');
		var selector = event.target;
		this._selectedObjectIDs = this._selectors.collect(function(node) {
			if (node.hasClassName('selected')) return node.getAttribute('objectID');
		}).filter(function(x) {return x});
		this._scratch.innerHTML = '';
		this._scratch.fire('selector:released');
		$('scratch').hide()
	},
	toggleSelector: function(event) {
		var node = event.target;
		var action = node.hasClassName('selected') ? 'remove' : 'add';
		node[action + 'ClassName']('selected');
	},
	getSelectedObjectIDs: function() {
		return this._selectedObjectIDs;
	},
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
	}	
});
gs.tracerize('MultipleObjectSelector', mod.MultipleObjectSelector);
    
})();
