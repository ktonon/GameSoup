/*
 * Type: Container
 * An object that simply contains another object.
 */
gamesoup.library.types.Container = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.Container.addMethods({
    
    /*---------------------------------------->                        Readable
     * read() : []
     * 
     * Read this content of this object.
     */                                                               /* vVv */
    read: function() {
        return this._value;
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Writable
     * write(item : [])
     * 
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
gamesoup.library.types.Container.addMethods({ 
    
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
gamesoup.library.types.Container.addMethods({
    // Helper methods go here...
});