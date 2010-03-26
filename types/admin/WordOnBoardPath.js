/*
 * Type: WordOnBoardPath
 * Give a word, can a sequence of adjacent cells be found on a board where letters on those cells spell out the word?
 */
gamesoup.library.types.WordOnBoardPath = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************///                                 REFERENCES                                
// this._board                                      -- Board
// this._word                                       -- Readable


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    
    /*
     * Boolean call()                               -- used in Predicate
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        return true
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    // Helper methods go here...
});