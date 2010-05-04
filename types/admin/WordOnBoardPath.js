/*
 * Type: WordOnBoardPath
 * Give a word, can a sequence of adjacent cells be found on a board where letters on those cells spell out the word?
 */
gamesoup.library.types.WordOnBoardPath = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._board                           [Board<cell=[Readable<item=String!>]>]
// this._word                                          [Readable<item=String!>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    
    /*---------------------------------------->                       Predicate
     * call() : Boolean!
     * 
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        var c = {};
        c.word = this._word.read();
        if (c.word.length == 0) {
            this._lastReason = "Please type your word in.";
            return false;
        } else {
            this._lastReason = this._failReason.evaluate(c);            
        }
        return true;
    },                                                                /* ^A^ */

    /*---------------------------------------->                       Predicate
     * reason() : String!
     * 
     * What was the reason for the last answer this predicate gave?
     */                                                               /* vVv */
    reason: function() {
        return this._lastReason;
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
        this._failReason = new Template("The word '#{word}' was not on the board");
        this._successReason = new Template("The word '#{word}' was found!");
        this._lastReason = "";
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    // Helper methods go here...
});