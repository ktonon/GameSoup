/*
 * Type: Label
 * A simple way to place text on the screen. The value never changes throughout the game.
 */
gamesoup.library.types.Label = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                Parameters                                
/*****************************************************************************/
//                                BUILT-INS                                 
// this._value                                      -- String

/*****************************************************************************/
/*                            Interface Methods                             
/*****************************************************************************/
gamesoup.library.types.Label.addMethods({
    
    /*
     * Nothing render()                             -- used in Renderable
     */
    render: function() {
        
    }
});

/*****************************************************************************/
/*                          Implementation methods                          
/*                    Do not use outside of this module!                    
/*****************************************************************************/
gamesoup.library.types.Label.addMethods({
    // Helper methods go here...
});
