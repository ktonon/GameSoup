/*
 * Type: TextField
 * A text output field that can be updated during the game.
 */
gamesoup.library.types.TextField = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                            Interface Methods                             
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
/*                          Implementation methods                          
/*                    Do not use outside of this module!                    
/*****************************************************************************/
gamesoup.library.types.TextField.addMethods({
    // Helper methods go here...
});
