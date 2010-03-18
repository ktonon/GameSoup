(function() {
gamesoup.namespace('gamesoup.library.types');

var gs = gamesoup;
var mod = gamesoup.library.types;

mod.BaseType = Class.create({
    initialize: function(node) {
        this._node = $(node);
        console.log('BaseType')
    }
});

})();
