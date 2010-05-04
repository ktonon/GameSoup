/*
 * Type: TransferIf
 * Action that reads a string from a source and if it is ok, sends it to a receiver. The source is cleared.
 */
gamesoup.library.types.TransferIf = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._destination                                        [Writable<item=[]>]
// this._source                                             [Readable<item=[]>]
// this._validator                                                  [Predicate]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.TransferIf.addMethods({
    
    /*---------------------------------------->                          Action
     * doAction()
     * 
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        if (this._validator.call()) {
            // Success
            var item = this._source.read();
            this._destination.write(item);
        } else {
            // Failure
            gamesoup.matches.messageBoard.postLocally(this._validator.reason());
        }
        // Need support for multiple interfaces on parameters.
        // this._source.clear();
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.TransferIf.addMethods({ 
    
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
gamesoup.library.types.TransferIf.addMethods({
    // Helper methods go here...
});