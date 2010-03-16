exported.SquareGrid = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._colCount = this._node.down('.argument[name=colCount]').getAttribute('value');
		this._rowCount = this._node.down('.argument[name=rowCount]').getAttribute('value');
		// this._initializeDOM();
	},
	_initializeDOM: function() {
		this._node = new Element('div');
		this._node.addClassName('board')
		this._node.addClassName('square-grid');
	},
	/********************************************************/
	/* Interface
	/********************************************************/
	
	adjacentTo: function(cell) {

	},
	areAdjacent: function(a, b) {
		
	}
});
