(function() {
gamesoup.namespace('gamesoup.dialogs');

var gs = gamesoup;
var mod = gamesoup.dialogs;

mod.Dialog = Class.create({
	initialize: function(node, handlers, options) {
		this._node = $(node);
		this._handlers = handlers;
		this._options = options;
		this._header = this._node.down('h1');
		this._contentNode = this._node.down('.content');
		this._closeButton = this._node.down('.close-button');
		// Event handlers
		this._closeButton.observe('click', this.hide.bind(this));
		this._node.observe('dialog:requestClose', this.hide.bind(this));
		this._node.observe('dialog:systemChanged', function() {this._systemChanged = true}.bind(this));
		this._node.observe('dialog:requestSuspend', this.suspend.bind(this));
		this._node.observe('dialog:requestResume', this.resume.bind(this));
		// Dragdrop
		this._headerDraggable = new Draggable(this._node, {
			handle: this._header
		})
	},
	release: function() {
		this._closeButton.stopObserving();
		this._node.stopObserving();
		this._headerDraggable.destroy();
	},
	update: function(html) {
		if (this._currentHandler) {
			this._currentHandler.release();
			this._currentHandler = null;
		}
		this._contentNode.update(html);
		var node = this._contentNode.down();
		this._header.innerHTML = node.getAttribute('title');
		var HandlerClass = this._handlers[node.getAttribute('handler')];
		this._currentHandler = new HandlerClass(node, this._options);
	},
	clear: function() {
		this._contentNode.innerHTML = '';
	},
	hide: function() {
		if (this._systemChanged) {
			this._node.fire('assembler:refreshRequired');			
		}
		this._node.hide();
		$('curtain').hide();
	},
	show: function() {
		this._systemChanged = false;
		$('curtain').show();
		this._node.show();
	},
	suspend: function() {
		this._node.hide();
	},
	resume: function() {
		this._node.show();
	}
});
gs.tracerize('Dialog', mod.Dialog);

})();
