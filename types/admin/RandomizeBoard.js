/*
 * Type: RandomizeBoard
 * Replace the contents of each cell on a board with a random object.
 */
gamesoup.library.types.RandomizeBoard = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************///                                 REFERENCES                                
// this._board                                      -- Board
// this._distribution                               -- RandomDistribution


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.RandomizeBoard.addMethods({
    
    /*
     * Nothing call()                               -- used in Action
     * Performs this default action of it's object.
     */
    call: function() {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.RandomizeBoard.addMethods({ 
    
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
gamesoup.library.types.RandomizeBoard.addMethods({
    // Helper methods go here...
});