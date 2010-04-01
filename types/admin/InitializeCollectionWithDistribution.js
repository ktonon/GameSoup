/*
 * Type: InitializeCollectionWithDistribution
 * For each writable cell in a collection, provide a newly instantiated object from a random distribution.
 */
gamesoup.library.types.InitializeCollectionWithDistribution = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._collection                          Iterable<item=Writable<item=item>>
// this._distribution                                   Distribution<item=item>


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.InitializeCollectionWithDistribution.addMethods({
    
    /*---------------------------------------->                          Action
     * doAction()
     * 
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        this._collection.resetIteration();
        var writableObj = this._collection.nextInIteration()
        while (writableObj) {
            var item = this._distribution.getRandomObject();
            writableObj.write(item);
            writableObj = this._collection.nextInIteration();
        }
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.InitializeCollectionWithDistribution.addMethods({ 
    
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
gamesoup.library.types.InitializeCollectionWithDistribution.addMethods({
    // Helper methods go here...
});