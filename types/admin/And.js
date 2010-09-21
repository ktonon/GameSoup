/*
 * Type: And
 * Ensure that both conditions are true.
 */
gamesoup.library.types.And = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._a                                                          [Predicate]
// this._b                                                          [Predicate]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.And.addMethods({
    
    /*---------------------------------------->                       Predicate
     * call() : Boolean!
     * 
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        if(this._a.call()) {
            if(this._b.call()) {
                this._reason = this._a.reason() + ' and ' + this._b.reason();
                return true;
            } else {
                this._reason = this._b.reason();
                return false;
            }
        } else {
            this._reason = this._a.reason();
            return false;
        }
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
gamesoup.library.types.And.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        
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
gamesoup.library.types.And.addMethods({
    // Helper methods go here...
});