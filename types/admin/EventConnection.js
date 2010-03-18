/*
 * Type: EventConnection
 * Call an action when an observed object fires an event.
 */
gamesoup.library.types.EventConnection = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                Parameters                                
/*****************************************************************************/
//                                BUILT-INS                                 
// this._event                                      -- String
//                                REFERENCES                                
// this._action                                     -- Action
// this._observed                                   -- Any

/*****************************************************************************/
/*                            Interface Methods                             
/*****************************************************************************/
gamesoup.library.types.EventConnection.addMethods({
    
    /*
     * Nothing register()                           -- used in Registerable
     */
    register: function() {
        
    }
});

/*****************************************************************************/
/*                          Implementation methods                          
/*                    Do not use outside of this module!                    
/*****************************************************************************/
gamesoup.library.types.EventConnection.addMethods({
    // Helper methods go here...
});
