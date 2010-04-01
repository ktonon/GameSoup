/*
 * Type: Cell
 * A simple type used to contain another
 */
gamesoup.library.types.Cell = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.Cell.addMethods({
    
    /*---------------------------------------->                        Readable
     * read() : item
     * 
     * Read this content of this object.
     */                                                               /* vVv */
    read: function() {
        return this._item;
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Writable
     * write(item : item)
     * 
     * Write a value to the content of this object.
     */                                                               /* vVv */
    write: function(item) {
        this._item = item;
        this._node.innerHTML = item;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.Cell.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._item = null;
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.Cell.addMethods({
    // Helper methods go here...
});