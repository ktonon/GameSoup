/*
 * Type: GameStart
 * Connect an action to this object to have it execute at the start of the game.
 */
gamesoup.library.types.GameStart = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************///                                 REFERENCES                                
// this._action                                     -- Action


/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.GameStart.addMethods({ 
    
    /*
     * Perform custom initialization.
     */
    register: function() {
         $('gamesoup-engine').observe('game:start', this._action.doAction.bind(this._action));
    }
    
});

/*****************************************************************************/
/*                           Implementation methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.GameStart.addMethods({
    // Helper methods go here...
});