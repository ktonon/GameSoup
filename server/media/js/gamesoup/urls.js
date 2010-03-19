(function() {
gamesoup.namespace('gamesoup.utils');

// Aliases for internal use
var gs = gamesoup;
var mod = gamesoup.utils;

mod.urls = $H({
	// Assembler
	refreshAssembler: new Template('/admin/games/game/#{gameID}/refresh-assembler/'),
    instantiateType: new Template('/admin/games/game/#{gameID}/type/#{typeID}/instantiate/'),
	updateObjectPosition: new Template('/admin/games/game/#{gameID}/object/#{objectID}/update-position/'),
	updateObjectSize: new Template('/admin/games/game/#{gameID}/object/#{objectID}/update-size/'),
	toggleObjectOwnership: new Template('/admin/games/game/#{gameID}/object/#{objectID}/toggle-ownership/'),
	objectConfigureDialog: new Template('/admin/games/game/#{gameID}/object/#{objectID}/configure/'),
	deleteObject: new Template('/admin/games/game/#{gameID}/object/#{objectID}/delete/'),
	saveParameterBinding: new Template('/admin/games/game/#{gameID}/object/#{objectID}/parameter/#{parameterID}/save/'),
	candidateRefs: new Template('/admin/games/game/#{gameID}/object/#{objectID}/parameter/#{parameterID}/candidate-refs/'),
	// Searching
	searchRequires: new Template('/admin/games/search-requires/'),
	searchRequiredBy: new Template('/admin/games/search-required-by/'),
	searchRequiredByParameter: new Template('/admin/games/search-required-by-parameter/#{parameterID}/'),
	browseTypes: new Template('/admin/library/type/')
});

mod.makeURL = function(urlName, context) {
    gs.assert (mod.urls.keys().member(urlName), 'Unregistered URL: ' + urlName + '\nPossibilities are: ' + mod.urls.keys());
    return mod.urls.get(urlName).evaluate(context);
}

})();
