(function() {
gamesoup.namespace('gamesoup.library.mixins');

var gs = gamesoup;
var mod = gamesoup.library.mixins;

mod.Visible = {
    isVisible: function() {
        return true;
    },
    setPosition: function(x, y) {
        this._x = x * gs.gridSize;
        this._y = y * gs.gridSize;
    },
    setSize: function(width, height) {
        this._width = width * gs.gridSize;
        this._height = height * gs.gridSize;
    },
    scale: function() {
        this._node.setStyle({
            position: 'absolute',
            left: this._x + 'px',
            top: this._y + 'px',
            width: this._width + 'px',
            height: this._height + 'px'
        });
    }
};

mod.Stateful = {
    isStateful: function() {
        return true;
    },
    setStatePerPlayer: function() {
        
    }
};

})();
