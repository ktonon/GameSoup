(function() {
gamesoup.namespace('gamesoup.library.mixins');

var gs = gamesoup;
var mod = gamesoup.library.mixins;

mod.Visible = {
    isVisible: function() {
        return true;
    },
    setPosition: function(x, y) {
        this._x = x * 20;
        this._y = y * 20;
    },
    setSize: function(width, height) {
        this._width = width * 20;
        this._height = height * 20;
    },
    scale: function() {
        this._node.setStyle({
            position: 'absolute',
            left: this._x + 'px',
            top: this._y + 'px',
            width: this._width + 'px',
            height: this._height + 'px',
            background: '#999'
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
