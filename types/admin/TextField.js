/*
 * Type: TextField
 * A text output field that can be updated during the game.
 */
gamesoup.library.types.TextField = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.TextField.addMethods({
    
    /*
     * Item read()                                  -- used in ReadWrite, Readable
     * Read this content of this object.
     */                                                               /* vVv */
    read: function() {
        return this._value;
    },                                                                /* ^A^ */

    /*
     * write(Item item)                             -- used in ReadWrite, Writable
     * Write a value to the content of this object.
     */                                                               /* vVv */
    write: function(item) {
        this._value = item;
        this._node.innerHTML = item;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.TextField.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        
    },                                                                /* ^A^ */
    
    /*
     *
     */                                                               /* vVv */
    stateSchema: function() {
        
    },                                                                /* ^A^ */
    
    /*
     *
     */                                                               /* vVv */
    initialState: function() {
        
    },                                                                /* ^A^ */
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._value = "";
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.TextField.addMethods({
    // Helper methods go here...
});