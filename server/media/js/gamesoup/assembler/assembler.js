(function() {
gamesoup.namespace('gamesoup.builder');

var gs = gamesoup;
var mod = gamesoup.builder;


gs.gridSize = 20;


mod.assembler = null;
mod.Assembler = Class.create({
	initialize: function(node) {
		this._node = $(node);
		this._gameName = this._node.getAttribute('gameName');
		this._setupDialogs();
		this._setupConfiguration();
		this._setupCanvas();
		var amd = mod.dialogs['add-modules'];
		$('clone-area').observe('click', this.saveParameterSetting.bind(this));
	},
	/********************************************************/
	/* INITIALIZATION
	/********************************************************/
	_setupDialogs: function() {
		$$('.dialog').each(mod.dialogForNode.curry(this._gameName));
		var amd = mod.dialogs['add-modules'];
		var rmd = mod.dialogs['remove-module'];
		this._addModuleChooser = new mod.ModuleChooser(amd);
		// Watch for changes that require an update.
		$('dialogs').observe('dialog:submitted', this.update.bind(this));
	},
	_setupConfiguration: function() {
		this._configNode = $('configuration');
		this._config = {};
		this._configNode.select('.object-configuration').each(function(node) {
			var objConf = new mod.ObjectConfiguration(node);
			this._config[objConf.getObjectID()] = objConf;
		}.bind(this));
		this._configNode.observe('object:removalRequested', this.showObjectRemovalDialog.bind(this));
		this._configNode.observe('object:builtInParameterSettingRequest', this.showBuiltInParameterSettingDialog.bind(this));
		this._configNode.observe('object:parameterSettingRequest', this.startParameterSettingMode.bind(this));
		this._configNode.observe('object:toggleOwnershipRequest', this.toggleObjectOwnership.bind(this));
	},
	_setupCanvas: function() {
		this._canvasNode = $('canvas');
		this._canvas = {};
		this._canvasNode.select('.object-shaper').each(function(node) {
			var objShaper = new mod.ObjectShaper(node);
			this._canvas[objShaper.getObjectID()] = objShaper;
		}.bind(this));
	},
	/********************************************************/
	/* UPDATING COMPONENTS
	/********************************************************/
	// Just doing this with a page refresh, because that is
	// easiest.
	update: function(transport) {
		window.location = '.';
	},
	/********************************************************/
	/* PARAMETER SETTINGS -- CONNECTING OBJECTS
	/********************************************************/
	startParameterSettingMode: function(event) {
		event.stop();
		var node = event.target;
		var variableID = node.getAttribute('variableID');
		var objectID = node.up('.object').getAttribute('objectID');
		var obj = this._canvas[objectID];
		var options = {
			objectID: objectID,
			variableID: variableID			
		};
		var url = gs.utils.makeURL('getPossibleParameterSettings', options);
		new Ajax.Request(url, {
			method: 'get',
			evalJS: true,
			onSuccess: function(options, transport) {
				Object.extend(options, transport.responseJSON);
				if (options.components.length == 0) {
					console.log('failed');
				} else {
					this.highlightPossibleParameterSettings(options);
				}
			}.bind(this, options)
		})
	},
	highlightPossibleParameterSettings: function(options) {
		$('curtain').show()
		options.components.each(function(options, pk) {
			var id = options.componentType + '-' + pk;
			var original = $(id);
			// Clone
			var copy = new Element('div');
			copy.addClassName('clone');
			$('clone-area').insert({top: copy});
			copy.clonePosition(original, {
				setWidth: false,
				setHeight: false
			});
			var button = new Element('input', {
				type: 'button',
				value: 'Set',
				objectID: options.objectID,
				variableID: options.variableID,
				argumentID: pk
				});
			copy.insert({top: button});
			console.log(copy)
		}.bind(this, options))
	},
	saveParameterSetting: function(event) {
		var node = event.target;
		if (node.up('.clone')) {
			var options = {
				objectID: node.getAttribute('objectID'),
				variableID: node.getAttribute('variableID')
			};
			var argumentID = node.getAttribute('argumentID');
			var url = gs.utils.makeURL('setParameter', options);
			new Ajax.Request(url, {
				method: 'post',
				postBody: 'component_id=' + argumentID,
				onSuccess: this.endParameterSettingMode.bind(this),
				onFailure: function(transport) {$('canvas').innerHTML = transport.responseText}
			});
		}
	},
	endParameterSettingMode: function(transport) {
		$$('#clone-area .clone').invoke('remove');
		$('curtain').hide();
		this.update();		
	},
	/********************************************************/
	/* OTHER OBJECT INTERACTIONS
	/********************************************************/
	toggleObjectOwnership: function(event) {
		event.stop();
		var node = event.target;
		var objectID = node.getAttribute('objectID');
		var obj = this._canvas[objectID]
		var url = gs.utils.makeURL('toggleObjectOwnership', {objectID: objectID});
		new Ajax.Request(url, {
			method: 'post',
			onSuccess: function(obj, transport) {
				obj.toggleOwnershipDisplay();
			}.bind(this, obj)
		})
	},
	/********************************************************/
	/* DIALOGS
	/********************************************************/
	showObjectRemovalDialog: function(event) {
		event.stop();
		var node = event.target;
		var id = node.getAttribute('objectID');
		var obj = this._canvas[id];
		var d = mod.dialogs['remove-object'];
		d.show({objectID: id}, {
			before: obj._node.addClassName.bind(obj._node, 'red-highlight'),
			after: obj._node.removeClassName.bind(obj._node, 'red-highlight'),
		});
	},
	showBuiltInParameterSettingDialog: function(event) {
		event.stop();
		var node = event.target;
		var variableID = node.getAttribute('variableID');
		var objectID = node.up('.object').getAttribute('objectID');
		var obj = this._canvas[objectID];
		var d = mod.dialogs['set-built-in-parameter'];
		d.show({objectID: objectID, variableID: variableID}, {
			before: obj._node.addClassName.bind(obj._node, 'green-highlight'),
			after: function(obj) {
				obj._node.removeClassName('green-highlight');
				this.update();
			}.bind(this, obj)
		});
	}
});
gs.tracerize('Assembler', mod.Assembler);


// Mixin for highlighting builder components that represent the same object
mod.ObjectHighlighter = {
	installHighlighter: function(componentType) {
		var titleNode = this._node.down('.title');
		titleNode.observe('click', this.toggleHighlightMembers.bind(this, {action: 'add'}));
		titleNode.observe('mouseout', this.toggleHighlightMembers.bind(this, {action: 'remove'}));	
	},
	toggleHighlightMembers: function(options) {
		options = options || {}
		var action = options.action + 'ClassName';
		var className = options.className || 'highlight';
		var name = this._node.getAttribute('objectID');
		$$('[objectID=' + name + ']').invoke(action, className);
	}	
};


mod.ModuleChooser = Class.create({
	initialize: function(dialog) {
		this._dialog = dialog;
		this._dialog._node.observe('dialog:reset', this.reset.bind(this));
	},
	reset: function() {
		this._selectNode = this._dialog._node.down('select[name="modules"]');
		this._previewNode = this._dialog._node.down('.preview');
		this._selectNode.observe('change', this.updatePreview.bind(this));
	},
	updatePreview: function(event) {
		var name = this._selectNode.getValue()[0];
		if (name) {
			var url = gamesoup.utils.makeURL('previewModuleQuick', {moduleName: name});
			new Ajax.Updater(this._previewNode, url);
		}
	}
});
gs.tracerize('ModuleChooser', mod.ModuleChooser);


document.observe('dom:loaded', function() {
	gamesoup.builder.assembler = new gamesoup.builder.Assembler('assembler');
});
})();