/*
 * Type: WordInDictionary
 * Is the given word in the given dictionary?
 */
gamesoup.library.types.WordInDictionary = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._dictionary                                                [Dictionary]
// this._word                                          [Readable<item=String!>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.WordInDictionary.addMethods({
    
    /*---------------------------------------->                       Predicate
     * call() : Boolean!
     * 
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        var word = this._word.read();
        var status = this._dictionary.hasWord(word);
        this._reason = (status ? this._successReason : this._failReason).evaluate({word: word});
        return status;
    },                                                                /* ^A^ */

    /*---------------------------------------->                       Predicate
     * reason() : String!
     * 
     * What was the reason for the last answer this predicate gave?
     */                                                               /* vVv */
    reason: function() {
        return this._reason;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.WordInDictionary.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._successReason = new Template('#{word} is in the dictionary');
        this._failReason = new Template('#{word} is not in the dictionary');
    },                                                                /* ^A^ */

    /*
     * Perform custom take-down.
     */                                                               /* vVv */
    unregister: function() {
        
    }                                                                 /* ^A^ */    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.WordInDictionary.addMethods({
    // Helper methods go here...
});