(function() {
gamesoup.namespace('gamesoup.layout');

var gs = gamesoup;
var mod = gamesoup.layout;

mod.TabSet = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._tabs = this._node.select('.tab').collect(this.addTab.bind(this));
		this._node.observe('tab:requestFocus', this.focusTab.bind(this));
	},
	addTab: function(node) {
		return new mod.Tab(node)
	},
	focusTab: function(event) {
		var node = event.target;
		this._tabs.invoke('demote');
		node.setStyle({zIndex: 10});
	}
});
gs.tracerize('TabSet', mod.TabSet);

mod.Tab = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._handleNode = this._node.down('h1.handle');
		// Events
		this._handleNode.observe('click', function() {this._node.fire('tab:requestFocus')}.bind(this));
	},
	demote: function() {
		var z = new Number(this._node.getStyle('z-index'));
		z = z > 0 ? z - 1 : 0;
		this._node.setStyle({zIndex: z});
	}
});
gs.tracerize('Tab', mod.Tab);

})();
