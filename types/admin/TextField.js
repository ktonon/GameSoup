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
     * String read()                                -- used in ReadWrite, Readable
     */
    read: function() {
        
    },

    /*
     * Nothing receive(Any object)                  -- used in Receiver
     */
    receive: function(object) {
        
    },

    /*
     * Nothing render()                             -- used in Renderable
     */
    render: function() {
        
    },

    /*
     * Nothing write(String w)                      -- used in ReadWrite, Writable
     */
    write: function(w) {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.TextField.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */
    render: function() {
        // this._node has already been created by this point
        
    },
    
    stateSchema: function() {
        
    },
    
    initialState: function() {
        
    },
    
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
gamesoup.library.types.TextField.addMethods({
    // Helper methods go here...
});