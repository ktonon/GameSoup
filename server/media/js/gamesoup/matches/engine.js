(function() {
gamesoup.namespace('gamesoup.matches');

var gs = gamesoup;
var mod = gamesoup.matches;

mod.Engine = Class.create({
    initialize: function(node) {
        this._node = $(node);
        this.createObjectLists();
        this.createDOM();
        this._objects.invoke('register');
        // Start the game
        this._node.fire('game:start');
    },
    createObjectLists: function() {
        this._objects = $H(mod.objects).values();
        this._statefulObjects = this._objects.filter(function(obj) {return obj.isStateful()});
        this._visibleObjects = this._objects.filter(function(obj) {return obj.isVisible()});        
    },
    createDOM: function() {
        this._canvasNode = new Element('div', {id: 'gamesoup-canvas'});
        this._codeNode = new Element('div', {id: 'gamesoup-code', style: 'display: none'});
        this._node.insert({bottom: this._canvasNode});
        this._node.insert({bottom: this._codeNode});
        // Add objects to DOM
        this._objects.each(function(obj) {
            var node = obj.createDOM();
            var root = obj.isVisible() ? this._canvasNode : this._codeNode;
            root.insert({bottom: node});
        }.bind(this));
        // Scale and render visible objects
        this._visibleObjects.invoke('scale');
        this._visibleObjects.invoke('render');
    }
});
gs.tracerize('Engine', mod.Engine);


document.observe('dom:loaded', function() {
    gamesoup.matches.engine = new gamesoup.matches.Engine('gamesoup-engine');
});
})();
