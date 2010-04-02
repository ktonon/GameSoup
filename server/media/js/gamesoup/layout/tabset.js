(function() {
gamesoup.namespace('gamesoup.layout');

var gs = gamesoup;
var mod = gamesoup.layout;

mod.TabSet = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._tabs = this._node.select('.tab').collect(this.addTab.bind(this));
		this._node.observe('tab:requestFocus', this.focusTab.bind(this));
		document.observe('keydown', this.walk.bind(this));
	},
	release: function() {
		this._tabs.invoke('release');
		this._node.stopObserving('tab:requestFocus');
	},
	addTab: function(node) {
		return new mod.Tab(node)
	},
	focusTab: function(event) {
		var node = event.target;
		this._tabs.invoke('demote');
		node.setStyle({zIndex: 10});
		node.addClassName('current');
		this._currentTab = node;
	},
	/*
	 * Walk through tabs using left and right keys
	 */
	walk: function(event) {
	    var code = event.keyCode;
	    var other;
	    if (code == Event.KEY_LEFT) {
	        other = this._currentTab.previous();
	    } else if (code == Event.KEY_RIGHT) {
	        other = this._currentTab.next();
	    }
	    if (other) {
	        other.fire('tab:requestFocus');
	    }
    	
	}
});
gs.tracerize('TabSet', mod.TabSet);

mod.Tab = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._handleNode = this._node.down('h1.handle');
		// Events
		this._handleNode.observe('click', function() {this._node.fire('tab:requestFocus')}.bind(this));
		// Adjust layout
		this.adjustHeight();
	},
	release: function() {
		this._handleNode.stopObserving('click');
	},
	adjustHeight: function() {
	    var h = document.viewport.getHeight() - this._node.cumulativeOffset()[1] - 40;
	    this._node.setStyle({height: h + 'px'});
	},
	demote: function() {
		var z = new Number(this._node.getStyle('z-index'));
		z = z > 0 ? z - 1 : 0;
		this._node.setStyle({zIndex: z});
		this._node.removeClassName('current');
	}
});
gs.tracerize('Tab', mod.Tab);

})();
