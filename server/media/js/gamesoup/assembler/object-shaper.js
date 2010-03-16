(function() {
gamesoup.namespace('gamesoup.builder');

var gs = gamesoup;
var mod = gamesoup.builder;

// For positioning and resizing elements on the canvas.
mod.ObjectShaper = Class.create();
mod.ObjectShaper.addMethods(mod.ObjectHighlighter);
mod.ObjectShaper.addMethods({
	initialize: function(node) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._resizeNode = this._node.down('.resize');
		// Other initialization
		this._setPositionAndSize();
		this.installHighlighter();
		// Make draggable
		new Draggable(this._node, {
			handle: this._renderedNode,
			snap: 20,
			onEnd: this.savePosition.bind(this)
		});
		// Make resizeable
		if (this._resizeNode) {
			new Draggable(this._resizeNode, {
				handle: this._resizeNode,
				snap: 20,
				onEnd: this.saveSize.bind(this),
				onDrag: this.updateSize.bind(this)
			});			
		}
	},
	_setPositionAndSize: function() {
		var g = function(x) {return new Number(x)};
		this._pos = this._node.getAttribute('position').split(',').collect(g);
		this._size = this._node.getAttribute('size').split(',').collect(g);
		this._node.setStyle({
			left: this._pos[0] * gs.gridSize + 'px', 
			top: this._pos[1] * gs.gridSize + 'px',
			width: this._size[0] * gs.gridSize - 2 + 'px',
			height: this._size[1] * gs.gridSize - 2 + 'px'
		});
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
	savePosition: function() {
		var x = gs.utils.cssNumber(this._node, 'left') / gs.gridSize;
		var y = gs.utils.cssNumber(this._node, 'top') / gs.gridSize;
		var url = gs.utils.makeURL('updateObjectPosition', {objectID: this.getObjectID()})
		new Ajax.Request(url, {
			method: 'post',
			postBody: 'position=' + x + ',' + y
		})
	},
	updateSize: function() {
		var h = function(u, offset) {return (u * gs.gridSize + offset + 'px')};
		var width = this._g('left');
		var height = this._g('top');
		this._node.setStyle({
			width: h(width, -2),
			height: h(height, -2)
		});
	},
	saveSize: function() {
		var width = this._g('left');
		var height = this._g('top');
		if (width <= 1 || height <= 1) {
			// Revert the resizer
			this._node.setStyle({
				width: this._size[0] * gs.gridSize - 2 + 'px',
				height: this._size[1] * gs.gridSize - 2 + 'px'
			});
			this._resizeNode.setStyle({
				left: (this._size[0] - 1) * gs.gridSize + 'px',
				top: (this._size[1] - 1) * gs.gridSize + 'px'
			});
		} else {
			var url = gs.utils.makeURL('updateObjectSize', {objectID: this.getObjectID()});
			new Ajax.Request(url, {
				method: 'post',
				postBody: 'size=' + width + ',' + height,
				onSuccess: function(width, height, transport) {
					var h = function(u, offset) {return (u * gs.gridSize + offset + 'px')};
					this._node.setStyle({
						width: h(width, -2),
						height: h(height, -2)
					});
					this._size = [width, height];					
				}.bind(this, width, height)
			})
		}
	},
	/********************************************************/
	/* HELPERS
	/********************************************************/
	_g: function(style) {
		return (gs.utils.cssNumber(this._resizeNode, style) / gs.gridSize).round() + 1
	}
});
gs.tracerize('ObjectShaper', mod.ObjectShaper);
    
})();
