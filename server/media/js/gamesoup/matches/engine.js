(function() {
gamesoup.namespace('gamesoup.matches');

var gs = gamesoup;
var mod = gamesoup.matches;

mod.Engine = Class.create({
    initialize: function(node) {
        this._node = $(node);
        this._objects = $H(mod.objects).values();
        this._objects.each(function(obj) {
            this._node.insert({bottom: obj.createDOM()});
        }.bind(this));
    }
});


document.observe('dom:loaded', function() {
    gamesoup.matches.engine = new gamesoup.matches.Engine('gamesoup-game-engine');
});
})();
