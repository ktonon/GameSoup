/*
 * Type: TextIsNumber
 * Does the text read from the source represent a number?
 */
gamesoup.library.types.TextIsNumber = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._source                                        [Readable<item=String!>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.TextIsNumber.addMethods({
    
    /*---------------------------------------->                       Predicate
     * call() : Boolean!
     * 
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        this._lastValue = this._source.read();
        return /^\s*\-?\s*\d+(\.\d*)?$/.match(this._lastValue);
    },                                                                /* ^A^ */

    /*---------------------------------------->                       Predicate
     * reason() : String!
     * 
     * What was the reason for the last answer this predicate gave?
     */                                                               /* vVv */
    reason: function() {
        return (this._lastCallSucceeded ?
            this._successReason 
            : this._failReason).evaluate({value: this._lastValue});
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.TextIsNumber.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._failReason = new Template("#{value} is not a number");
        this._successReason = new Template("#{value} is a number");
        this._lastValue = null;
        this._lastCallSucceeded = false;
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
gamesoup.library.types.TextIsNumber.addMethods({
    // Helper methods go here...
});