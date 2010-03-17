(function() {
gamesoup.namespace('gamesoup.utils');

// Aliases for internal use
var gs = gamesoup;
var mod = gamesoup.utils;

mod.urls = $H({
	// Assembler
    instantiateObject: new Template('/admin/games/game/#{gameID}/type/#{typeID}/instantiate/'),
	updateObjectPosition: new Template('/admin/games/game/#{gameID}/object/#{objectID}/update-position/'),
	updateObjectSize: new Template('/admin/games/game/#{gameID}/object/#{objectID}/update-size/')
});

mod.makeURL = function(urlName, context) {
    gs.assert (mod.urls.keys().member(urlName), 'Unregistered URL: ' + urlName + '\nPossibilities are: ' + mod.urls.keys());
    return mod.urls.get(urlName).evaluate(context);
}

})();
