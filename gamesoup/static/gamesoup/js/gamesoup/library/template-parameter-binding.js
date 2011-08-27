(function() {
gamesoup.namespace('gamesoup.library.templation');

var gs = gamesoup;
var mod = gamesoup.library.templation;

mod.TemplateParameterBinding = Class.create({
    initialize: function(node) {
        this._node = $(node);
        this._selectNode = this._node.down('select');
        this._deleteBox = this._node.up().down('input[type=checkbox]');
    },
    update: function(html) {
        var value = this._selectNode.getValue();
        this._selectNode.update(html);
        var invalid = this._selectNode.select('option[value='+value+']').length == 0;
        if (invalid) {
            if (this._deleteBox) this._deleteBox.setValue(1);
        } else {
            this._selectNode.setValue(value);
        }
    }
});

mod.PossibleParameters = Class.create({
    initialize: function() {
        this._html;
    },
    refresh: function(ids) {
        new Ajax.Request('possible-template-parameters/', {
            method: 'post',
            postBody: 'ids=' + ids.join(','),
            evalJS: true,
            onSuccess: function(transport) {
                this._data = transport.responseJSON.possibilities;
                this._html = '<option value="">---------</option>';
                this._data.each(function(item) {
                    this._html += '<option value="' + item.id + '">' + item.name + '</option>';
                }.bind(this));
                mod.templateParameterBindings.invoke('update', this._html);
            }
        });
    }
});

mod.getIDs = function() {
    var node = $$('.filtered')[1];
    return node.select('option').collect(function(option) {
        return option.getAttribute('value')
    });
}

document.observe('dom:loaded', function() {
    mod.templateParameterBindings = $$('.inline-group .parameter').collect(function(node) {
        return new mod.TemplateParameterBinding(node);
    });
    mod.possibleParameters = new mod.PossibleParameters();

    // Rig SelectBox to call possibleParameters.refresh
    SelectBox.move = function(old_move, from, to) {
        old_move(from, to);
        mod.possibleParameters.refresh(mod.getIDs());
    }.curry(SelectBox.move);
    
});
})();

