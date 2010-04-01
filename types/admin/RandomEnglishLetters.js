/*
 * Type: RandomEnglishLetters
 * Distribution over the Latin alphabet. Generates letters in the frequency in which they occur in the English language.
 */
gamesoup.library.types.RandomEnglishLetters = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({
    
    /*---------------------------------------->                    Distribution
     * getRandomObject() : String
     * 
     * Return a random object from a distribution
     */                                                               /* vVv */
    getRandomObject: function() {
        return this._letters[(Math.random() * this._letters.length).floor()];
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._letters = "";
        var freqs = [82,15,28,43,127,22,20,61,70,2,8,40,24,67,75,19,1,60,63,91,28,10,24,2,20,1];
        freqs.zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ".toArray()).each(function(item) {
            var freq = item[0];
            var letter = item[1];
            this._letters += letter.times(freq);
        }.bind(this));
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({
    // Helper methods go here...
});