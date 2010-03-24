/*
 * Type: SubmitStringWithCheck
 * Action that reads a string from a source and if it is ok, sends it to a receiver. The source is cleared.
 */
gamesoup.library.types.SubmitStringWithCheck = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************///                                 REFERENCES                                
// this._destination                                -- Writable
// this._source                                     -- ReadWrite
// this._validator                                  -- Predicate


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.SubmitStringWithCheck.addMethods({
    
    /*
     * doAction()                                   -- used in Action
     * Perform the default action of this object.
     */
    doAction: function() {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.SubmitStringWithCheck.addMethods({ 
    
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
gamesoup.library.types.SubmitStringWithCheck.addMethods({
    // Helper methods go here...
});