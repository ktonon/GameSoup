(function() {
gamesoup.namespace('gamesoup.games.parameters');

var gs = gamesoup;
var mod = gamesoup.games.parameters;


mod.Parameter = Class.create({
	initialize: function(node, options) {
		this._node = $(node);
		this._paramID = this._node.getAttribute('parameterID');
		this._options = {parameterID: this._paramID};
		Object.extend(this._options, options);
		this._name = this._node.getAttribute('name');
		this._node.insert({bottom: '<label class="required">' + this._name + '</label>'});
	},
	release: function() {
		
	}
})


mod.BuiltIn = Class.create(mod.Parameter, {
	initialize: function($super, node, options) {
		$super(node, options);
		this._node.insert({top: '<ul class="errorlist"></ul>'});
		this._errorListNode = this._node.down('.errorlist');
		this._interfaceName = this._node.getAttribute('interface');
		this._originalValue = this._node.getAttribute('value');
		this.createWidget();
		this._widget.setValue(this._originalValue);
		// Event handlers
		this._widget.observe('change', this.save.bind(this));
	},
	findErrors: function() {
		return [];
	},
	release: function() {
		this._widget.stopObserving();
	},
	showErrors: function(errors) {
		this._node.addClassName('errors');
		errors.each(function(message) {this._errorListNode.insert({bottom: '<li>' + message + '</li>'})}.bind(this));		
	},
	clearErrors: function() {
		this._node.removeClassName('errors');
		this._errorListNode.innerHTML = '';
	},
	save: function() {
		this.clearErrors();
		var errors = this.findErrors();
		if (errors.length) {
			this.showErrors(errors);
		} else {
			var url = gs.utils.makeURL('saveParameterBinding', this._options);
			new Ajax.Request(url, {
				method: 'post',
				postBody: 'value=' + this.getValue(),
				onSuccess: function() {this._node.fire('assembler:systemChanged')}.bind(this)
			});
		}
	}
})


mod.String = Class.create(mod.BuiltIn, {
	initialize: function($super, node, options) {
		$super(node, options);
	},
	createWidget: function() {
		this._node.insert({bottom: '<input type="text" value="" />'});
		this._widget = this._node.down('input');		
	},
	getValue: function() {
		return this._widget.getValue();
	},
	findErrors: function($super) {
		var errors = $super();
		var value = this._widget.getValue();
		if (!value) errors.push('This parameter is required');
		return errors;
	}
});
gs.tracerize('String', mod.String);


mod.Integer = Class.create(mod.String, {
	initialize: function($super, node, options) {
		$super(node, options);
	},
	createWidget: function() {
		this._node.insert({bottom: '<input type="text" value="" style="width: 50px" />'});
		this._widget = this._node.down('input');		
	},
	findErrors: function($super) {
		var errors = $super();
		var value = this._widget.getValue();
		if (value.match(/^\d*$/) == null) errors.push('Please enter a positive integer');
		return errors;
	}
})
gs.tracerize('Integer', mod.Integer);


mod.Float = Class.create(mod.String, {
	initialize: function($super, node, options) {
		$super(node, options);
	},
	createWidget: function() {
		this._node.insert({bottom: '<input type="text" value="" style="width: 50px" />'});
		this._widget = this._node.down('input');		
	},
	findErrors: function($super) {
		var errors = $super();
		var value = this._widget.getValue();
		if (value.match(/^(\d+(\.\d+)?)?$/) == null) errors.push('Please enter a positive decimal number');
		return errors;
	}
})
gs.tracerize('Float', mod.Float);

    
mod.Reference = Class.create(mod.Parameter, {
	initialize: function($super, node, options) {
		$super(node, options);
		this.createWidget();
		this._boundToDisclosure.update(this._node.getAttribute('boundTo'));
		// Event handlers
		this._widget.observe('click', this.bindRef.bind(this));			
	},
	release: function() {
		this._widget.stopObserving();
	},
	createWidget: function() {
		this._node.insert({bottom: '<input type="button" value="Bind" title="Bind this parameter to an object." /> <span class="bound-to-disclosure"></span>'});
		this._widget = this._node.down('input');
		this._boundToDisclosure = this._node.down('.bound-to-disclosure');
	},
	setValue: function(value) {
		this._node.setAttribute('boundTo', value);
		this._boundToDisclosure.update(value);
	},
	getValue: function() {
		return this._node.getAttribute('boundTo');
	},
	bindRef: function() {
		var url = gs.utils.makeURL('candidateRefs', this._options);
		new Ajax.Request(url, {
			method: 'get',
			evalJS: true,
			onSuccess: function(transport) {
				var objects = transport.responseJSON.collect(function(id) {return $(id)});
				gs.games.messageBox.post('Please bind ' + this._name + ' to one of the following objects...');
				new gamesoup.games.selectors.SingleObjectSelector(objects, function(objectID) {
				    // Called after the selector returns
					gs.games.messageBox.clear();
					this.setValue(objectID);
					this.save();
				}.bind(this));
			}.bind(this)
		});
	},
	save: function() {
		var url = gs.utils.makeURL('saveParameterBinding', this._options);
		new Ajax.Request(url, {
			method: 'post',
			evalJS: true,
			postBody: 'value=' + this.getValue(),
			onSuccess: function(transport) {
			    this._boundToDisclosure.update(transport.responseJSON.value);
			    this._node.fire('assembler:systemChanged')
			}.bind(this)
		});
	}	
});
gs.tracerize('Reference', mod.Reference);


// What this one does:
//   * Query the server for types that can satisfy this reference
//   * Let the user pick a type from the popup
//   * Drop the chosen type id into a dropbox
//   * Instantiate an object for that type
//   * Bind the parameter to the newly instantiated object
mod.UnsatisfiableReference = Class.create(mod.Parameter, {
    initialize: function($super, node, options) {
        $super(node, options);
		this.createWidget();
		// Event handlers
		this._widget.observe('click', this.search.bind(this));
		this._watchForNewObject = this.bindNewObject.bind(this);
		$('assembler').observe('assembler:objectAdded', this._watchForNewObject);
	},
	release: function() {
		this._widget.stopObserving('click');
		$('assembler').stopObserving('assembler:objectAdded', this._watchForNewObject);
	},
	createWidget: function() {
	    this._node.insert({bottom: '<input type="text" id="id_unsatref" style="display: none" />'});
		this._node.insert({bottom: '<input type="button" id="lookup_id_unsatref" value="Search" title="None of the objects in your game can satisfy this parameter. Search the library for one that does." />'});
        this._dropbox = this._node.down('input[type=text]');
		this._widget = this._node.down('input[type=button]');
	},
	search: function() {
		var url = gs.utils.makeURL('searchRequiredByParameter', this._options);
		new Ajax.Request(url, {
			method: 'get',
			evalJS: true,
			onSuccess: function(transport) {
				var type_ids = transport.responseJSON;
				this._widget.setAttribute('href', gs.utils.makeURL('browseTypes') + '?id__in=' + type_ids.join(','));
				showRelatedObjectLookupPopup(this._widget);
				// Now a popup appears with a list of possible types.
				// When the user selects a type, its id will get put into the dropbox
				// and 'dropbox:change' will fire.
				// The Assembler is already watching for this event and will take
				// care of instantiating the object and refreshing the page.
			}.bind(this)
		});
	},
	bindNewObject: function(event) {
	    var url = gs.utils.makeURL('saveParameterBinding', this._options);
		new Ajax.Request(url, {
			method: 'post',
			postBody: 'value=' + event.memo.objectID,
			onSuccess: function() {
        	    this.release();
        	    this._widget.replace(new Template('<span class="note">This parameter has been bound to the newly created #{typeName}.<span>').evaluate(event.memo));
			    this._node.fire('assembler:systemChanged');
			}.bind(this)
		});
	}	
});
gs.tracerize('UnsatisfiableReference', mod.UnsatisfiableReference);


mod.FactoryReference = Class.create(mod.Parameter, {
    initialize: function($super, node, options) {
        $super(node, options);
		this.createWidget();
		this._boundToDisclosure.update(this._node.getAttribute('boundTo'));
		// Event handlers
		this._widget.observe('click', this.search.bind(this));
		this._watchForType = this.bindType.bind(this);
		this._dropbox.observe('dropbox:change', this._watchForType);
	},
	release: function() {
		this._widget.stopObserving('click');
        this._dropbox.stopObserving('dropbox:change', this._watchForType);
	},
	createWidget: function() {
	    this._node.insert({bottom: '<input type="text" id="id_factoryref" style="display: none" />'});
		this._node.insert({bottom: '<input type="button" id="lookup_id_factoryref" value="Search" title="Find a type to use as a factory." /> <span class="bound-to-disclosure"></span>'});
        this._dropbox = this._node.down('input[type=text]');
		this._widget = this._node.down('input[type=button]');
		this._boundToDisclosure = this._node.down('.bound-to-disclosure');
	},
	search: function() {
		var url = gs.utils.makeURL('searchRequiredByParameter', this._options);
		new Ajax.Request(url, {
			method: 'get',
			evalJS: true,
			onSuccess: function(transport) {
				var type_ids = transport.responseJSON;
				this._widget.setAttribute('href', gs.utils.makeURL('browseTypes') + '?id__in=' + type_ids.join(','));
				showRelatedObjectLookupPopup(this._widget);
				// Now a popup appears with a list of possible types.
				// When the user selects a type, its id will get put into the dropbox
				// and 'dropbox:change' will fire.
				// The Assembler is already watching for this event and will take
				// care of instantiating the object and refreshing the page.
			}.bind(this)
		});
	},
	bindType: function(event) {
	    event.stop(); // Prevent other handlers from doing anyting with dropbox:change
		var typeID = this._dropbox.getValue();
        var url = gs.utils.makeURL('saveParameterBinding', this._options);
        new Ajax.Request(url, {
            method: 'post',
            evalJS: true,
            postBody: 'value=' + typeID,
            onSuccess: function(transport) {
                this._boundToDisclosure.update(transport.responseJSON.value);
                this._node.fire('assembler:systemChanged');
            }.bind(this)
        });
	}	
});
gs.tracerize('UnsatisfiableReference', mod.UnsatisfiableReference);

})();
