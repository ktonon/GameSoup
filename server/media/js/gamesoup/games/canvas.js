(function() {
gamesoup.namespace('gamesoup.games');

var gs = gamesoup;
var mod = gamesoup.games;

mod.Canvas = Class.create();
mod.Canvas.addMethods({
	initialize: function(node, options) {
		this._node = $(node);
		this._options = options;
		this._shapers = this._node.select('.object-shaper').collect(this.addShaper.bind(this));
	},
	release: function() {
		this._shapers.invoke('release');
	},
	addShaper: function(node) {
		return new mod.ObjectShaper(node, this._options);
	}
});
gs.tracerize('Canvas', mod.Canvas);


// For positioning and resizing elements on the canvas.
mod.ObjectShaper = Class.create();
// mod.ObjectShaper.addMethods(mod.ObjectHighlighter);
mod.ObjectShaper.addMethods({
	initialize: function(node, options) {
		this._node = $(node);
		this._objectID = this._node.getAttribute('objectID');
		this._options = {objectID: this._objectID};
		Object.extend(this._options, options);
		this._resizeNode = this._node.down('.resize');
		// Other initialization
		this._setPositionAndSize();
		// this.installHighlighter();
		// Make shapers
		this._positionDraggable = new Draggable(this._node, {
			handle: this._renderedNode,
			snap: 20,
			onEnd: this.savePosition.bind(this),
			onDrag: this.updatePosition.bind(this)
		});
		this._sizeDraggable = new Draggable(this._resizeNode, {
			handle: this._resizeNode,
			snap: 20,
			onEnd: this.saveSize.bind(this),
			onDrag: this.updateSize.bind(this)
		});			
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
	release: function() {
		this._positionDraggable.destroy();
		this._sizeDraggable.destroy();
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
	updatePosition: function() {
		var x = gs.utils.cssNumber(this._node, 'left') / gs.gridSize;
		var y = gs.utils.cssNumber(this._node, 'top') / gs.gridSize;
		mod.messageBox.post('(' + x + ', ' + y + ')');
	},
	savePosition: function() {
		var x = gs.utils.cssNumber(this._node, 'left') / gs.gridSize;
		var y = gs.utils.cssNumber(this._node, 'top') / gs.gridSize;
		var url = gs.utils.makeURL('updateObjectPosition', this._options)
		new Ajax.Request(url, {
			method: 'post',
			postBody: 'position=' + x + ',' + y
		});
		mod.messageBox.clear();
	},
	updateSize: function() {
		var h = function(u, offset) {return (u * gs.gridSize + offset + 'px')};
		var width = this._g('left');
		var height = this._g('top');
		this._node.setStyle({
			width: h(width, -2),
			height: h(height, -2)
		});
		mod.messageBox.post(width + ' x ' + height);
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
			var url = gs.utils.makeURL('updateObjectSize', this._options);
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
		mod.messageBox.clear();
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
