(function() {
gamesoup.namespace('gamesoup.utils');

// Aliases for internal use
var gs = gamesoup;
var mod = gamesoup.utils;

document.observe('dom:loaded', function() {
    $$('a.popup').each(function(node) {
        node.observe('click', function(node, event) {
            event.stop();
            var href = node.getAttribute('href') + '?_popup=1';
            var win = window.open(href, 'popup', 'height=500,width=800,resizable=yes,scrollbars=yes');
            win.focus();
            return false;
        }.curry(node));
    })
});

})();
