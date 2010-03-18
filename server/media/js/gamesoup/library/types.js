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
        this._node.innerHTML = this._id;
        return this._node;
    }
});

})();
