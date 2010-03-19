(function() {
gamesoup.namespace('gamesoup.games');

var gs = gamesoup;
var mod = gamesoup.games;


mod.Assembler = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._gameID = this._node.getAttribute('gameID');
		this._options = {gameID: this._gameID};
		this._tabset = new gs.layout.TabSet(this._node);
		this._objects = new mod.ObjectList('object-list', this._options);
		this._canvas = new mod.Canvas('canvas', this._options);
		this._dialog = new gs.dialogs.Dialog('dialog', mod.dialogHandlers, this._options);
		this._refresherNode = new Element('div', {style: 'display: block'});
		this._node.insert({bottom: this._refresherNode});
		// Object creators
		this._searchRequires = $('lookup_id_search_requires');
		this._searchRequiredBy = $('lookup_id_search_required_by');
		this._idDropboxes = $$('.id-dropbox');
		// Event handlers
		this._searchRequires.observe('click', this.search.bind(this, gs.utils.makeURL('searchRequires'), 'Find objects that require all of the selected objects as parameters. Select one or more and click "Search".'));
		this._searchRequiredBy.observe('click', this.search.bind(this, gs.utils.makeURL('searchRequiredBy'), 'Find objects that satisfy at least one parameter on all of the selected objects. Select one or more and click "Search"'));
		this._node.observe('object:requestConfig', this.showObjectConfigDialog.bind(this));
		this._node.observe('object:requestDeletion', this.deleteObject.bind(this));
		// As the game configuration changes the Assembler will
		// get out of sync with those changes. The easiest way to
		// fix this is to completely reset it. Instead of doing
		// a page refresh, which requires all scripts to be reloaded,
		// we can query the server for the updated DOM of the object list
		// and canvas, and then recreate the javascript wrappers from them.
		$('content-main').observe('assembler:refreshRequired', this.refresh.bind(this));
		// Assumes that all dropboxes are used for collecting
		// type ids which need to be instantiated into objects
		// When the object gets added to the game, addObjectToGame
		// will fire 'assembler:objectAdded', which can be used
		// to perform actions afterwards such as binding that object
		// to other objects.
        $('content-main').observe('dropbox:change', function(event) {
			var dropbox = event.target;
			var id = dropbox.getValue();
			this.addObjectToGame(id);
		}.bind(this));
	},
	release: function() {
		this._tabset.release();
		this._objects.release();
		this._canvas.release();
		this._dialog.release();
		this._node.stopObserving();
		$('content-main').stopObserving('assembler:refreshRequired');
		this._idDropboxes.invoke('stopObserving');
	},
	addObjectToGame: function(id) {
		var options = {typeID: id};
		Object.extend(options, this._options);
		var url = gs.utils.makeURL('instantiateType', options);
		new Ajax.Request(url, {
			method: 'post',
			evalJS: true,
			onSuccess: function(transport) {
			    this.refresh();
			    this._node.fire('assembler:objectAdded', transport.responseJSON);
			}.bind(this)
		})
	},
	showObjectConfigDialog: function(event) {
		var node = event.target;
		var url = node.getAttribute('configURL');
		this._dialog.clear();
		this._dialog.show();
		new Ajax.Request(url, {
			method: 'get',
			onSuccess: function(transport) {
				this._dialog.update(transport.responseText);
			}.bind(this)
		});
	},
	deleteObject: function(event) {
		var node = event.target;
		var url = node.getAttribute('deleteURL');
		new Ajax.Request(url, {
			method: 'post',
			onSuccess: this.refresh.bind(this)
		});
	},
	refresh: function() {
		// Reload the object list and canvas
		// Calls release to make sure event handlers and draggables are removed
		var url = gs.utils.makeURL('refreshAssembler', this._options);
		new Ajax.Request(url, {
			method: 'get',
			onSuccess: function(transport) {
				this._refresherNode.update(transport.responseText);
				var refresher;
				// Reset the canvas
				this._canvas.release();
				refresher = this._refresherNode.down('.canvas-refresher');
				$('canvas').down('.content').replace(refresher.remove());
				refresher.removeClassName('.canvas-refresher');
				this._canvas = new mod.Canvas('canvas', this._options);
				// Reset the object list
				this._objects.release();
				refresher = this._refresherNode.down('.object-list-refresher');
				$('object-list').down('.content').replace(refresher.remove());
				refresher.removeClassName('.object-list-refresher');
				this._objects = new mod.ObjectList('object-list', this._options);				
			}.bind(this)
		});
	},
	search: function(url, message, event) {
		event.stop();
		var button = event.target;
		$('curtain').show();
		mod.messageBox.post(message);
		var selector = new gamesoup.games.selectors.MultipleObjectSelector($$('.object'));
		$('scratch').observe('selector:released', function(selector, url, button) {
			mod.messageBox.clear();
			$('scratch').stopObserving('selector:released');
			$('curtain').hide();
			var ids = selector.getSelectedObjectIDs();
			new Ajax.Request(url, {
				method: 'post',
				postBody: 'object_ids=' + ids.join(','),
				evalJS: true,
				onSuccess: function(button, transport) {
					var ids = transport.responseJSON;
					button.setAttribute('href', button.getAttribute('link') + '?id__in=' + ids.join(','));
					showRelatedObjectLookupPopup(button);
				}.bind(this, button)
			})
		}.bind(this, selector, url, button));
	}
});
gs.tracerize('Assembler', mod.Assembler);


mod.MessageBox = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._valueNode = this._node;
	},
	post: function(message) {
		this._valueNode.innerHTML = message;
	},
	clear: function() {
		this._valueNode.innerHTML = '';
	}
});
gs.tracerize('MessageBox', mod.MessageBox);


document.observe('dom:loaded', function() {
	gamesoup.games.messageBox = new gamesoup.games.MessageBox('message-box');
	gamesoup.games.assembler = new gamesoup.games.Assembler('assembler');
	$('canvas').fire('tab:requestFocus');
});
})();


// HACK
// Replace django's function with this one.
function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
	elem.fire('dropbox:change') // <== Customization
    win.close();
}

function showRelatedObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href = triggeringLink.getAttribute('href'); // <== Customization (allows use of non-anchors)
    if (href.search(/\?/) >= 0) {
        href += '&pop=1';
    } else {
        href += '?pop=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}