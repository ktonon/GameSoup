/*
 * Type: RandomEnglishLetters
 * Produces random Latin letters in the frequency appropriate for making English words.
 */
gamesoup.library.types.RandomEnglishLetters = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({
    
    /*
     * Any getRandomObject()                        -- used in RandomDistribution
     */
    getRandomObject: function() {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({ 
    
    /*
     * Perform custom initialization.
     */
    register: function() {
         
    }
    
});

/*****************************************************************************/
/*                           Implementation methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.RandomEnglishLetters.addMethods({
    // Helper methods go here...
});