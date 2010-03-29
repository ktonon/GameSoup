(function() {
gamesoup.namespace('gamesoup.library.types');

var gs = gamesoup;
var mod = gamesoup.library.types;

mod.BaseType = Class.create({
    initialize: function(id) {
        this._id = id;
    },
    createDOM: function() {
        this._node = new Element('div', {id: this._id});
        return this._node;
    },
    isVisible: function() {
        return false;
    },
    isStateful: function() {
        return false;
    },
    observe: function(eventName, action) {
        this._node.observe(eventName, action);
    }
});

})();
