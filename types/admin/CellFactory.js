/*
 * Type: CellFactory
 * A factory for creating cells.
 */
gamesoup.library.types.CellFactory = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.CellFactory.addMethods({
    
    /*
     * Item instantiate()                           -- used in Factory
     * Create an instance of a given type.
     */                                                               /* vVv */
    instantiate: function() {
        var cell = new gamesoup.library.types.Cell();
        cell.createDOM();
        cell.register();
        return cell;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.CellFactory.addMethods({ 
    
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
gamesoup.library.types.CellFactory.addMethods({
    // Helper methods go here...
});