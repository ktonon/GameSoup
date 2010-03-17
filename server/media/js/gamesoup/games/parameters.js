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
				onSuccess: function() {this._node.fire('parameter:saved')}.bind(this)
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
gs.tracerize('Text', mod.Text);


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
		if (!this._node.hasClassName('unsatisfiable')) {
			this.createWidget();
			this._boundToDisclosure.update(this._node.getAttribute('boundTo'));
			// Event handlers
			this._widget.observe('click', this.bindRef.bind(this));			
		} else {
			this._node.insert({bottom: '<div class="note">This parameter is unsatisfiable. Try using <strong>&ldquo;obj &rarr; x&rdquo;</strong> to find an appropraite object.</div>'});
		}
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
		this._node.fire('dialog:requestSuspend');
		var url = gs.utils.makeURL('candidateRefs', this._options);
		new Ajax.Request(url, {
			method: 'get',
			evalJS: true,
			onSuccess: function(transport) {
				var objects = transport.responseJSON.collect(function(id) {return $(id)});
				gs.games.messageBox.post('Please bind ' + this._name + ' to one of the following objects...');
				var selector = new gamesoup.games.selectors.SingleObjectSelector(objects);				
				$('scratch').observe('selector:released', function(selector) {
					gs.games.messageBox.clear();
					var objectID = selector.getSelectedObjectID();
					$('scratch').stopObserving('selector:released');
					this.setValue(objectID);
					this.save();
					this._node.fire('dialog:requestResume');
				}.bind(this, selector));
			}.bind(this)
		});
	},
	save: function() {
		var url = gs.utils.makeURL('saveParameterBinding', this._options);
		new Ajax.Request(url, {
			method: 'post',
			postBody: 'value=' + this.getValue(),
			onSuccess: function() {this._node.fire('parameter:saved')}.bind(this)
		});
	}	
});
gs.tracerize('Reference', mod.Reference);


})();
