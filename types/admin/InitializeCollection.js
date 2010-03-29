/*
 * Type: InitializeCollection
 * For each writable cell in a collection, provide a newly instantiated object.
 */
gamesoup.library.types.InitializeCollection = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._collection --                         Iterable&lt;Item=Any&gt;
// this._factory --                          Factory&lt;Item=Any&gt;


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.InitializeCollection.addMethods({
    
    /*
     * doAction()                                   -- used in Action
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        this._collection.resetIteration();
        var nextCell = this._collection.nextInIteration()
        while (nextCell) {
            var item = this._factory.instantiate();
            nextCell.write(item);
            nextCell = this._collection.nextInIteration();
        }
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.InitializeCollection.addMethods({ 
    
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
gamesoup.library.types.InitializeCollection.addMethods({
    // Helper methods go here...
});