(function() {
gamesoup.namespace('gamesoup.matches');

var gs = gamesoup;
var mod = gamesoup.matches;

mod.Engine = Class.create({
    initialize: function(node) {
        this._node = $(node);
        console.log('Engine loaded!');
    }
});


document.observe('dom:loaded', function() {
    gamesoup.matches.engine = new gamesoup.matches.Engine('gamesoup-game-engine');
});
})();
