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
		this._node.observe('handler:done', this.hide.bind(this));
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
	/*
	 * Open and close the dialog, protecting it with a transaction.
	 */
	hide: function() {
		this._node.hide();
		$('curtain').hide();
		$('content-main').stopObserving('selector:started', this._watchStarted);
		$('content-main').stopObserving('selector:completed', this._watchCompleted);
		this._node.fire('assembler:transactionCompleted');
	},
	show: function() {
		this._node.fire('assembler:transactionStarted');
		this._watchStarted = $('content-main').observe('selector:started', this.suspend.bind(this));
		this._watchCompleted = $('content-main').observe('selector:completed', this.resume.bind(this));
		$('curtain').show();
		this._node.show();
	},
	/*
	 * Suspend and resume temporarilly hide the dialog, but not the curtain.
	 * This is useful for using the curtain to keep the rest of the interface
	 * disabled, while using the scratch space on top of the curtain to
	 * present a custom interaction.
	 */
	suspend: function() {
		this._node.hide();
	},
	resume: function() {
		this._node.show();
	}
});
gs.tracerize('Dialog', mod.Dialog);

})();
