(function() {
gamesoup.namespace('gamesoup.matches');

var gs = gamesoup;
var mod = gamesoup.matches;

mod.MessageBoard = Class.create({
    initialize: function(node) {
        this._node = $(node);
        this._node.insert({bottom: '<ul></ul>'});
        this._listNode = this._node.down('ul');
    },
    postLocally: function(message, options) {
        options = Object.extend({
            duration: 2
        }, options);
        var item = new Element('li', {style: 'display: none'});
        item.innerHTML = message;
        this._listNode.insert({top: item});
        new Effect.Appear(item, {duration: 0.5})
        setTimeout(this.removeMessage.bind(this, item), options.duration * 1000);
    },
    removeMessage: function(itemNode) {
        new Effect.Fade(itemNode, {
            duration: 0.5,
            afterFinish: function(node) {
                node.remove();
            }.curry(itemNode)
        })
    }
});

})();
