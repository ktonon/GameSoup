/*
 * Type: EndGame
 * Action to end the game. When the game ends, a black semi-transparent sheet will block all game UI elements.
 */
gamesoup.library.types.EndGame = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.EndGame.addMethods({
    
    /*---------------------------------------->                          Action
     * doAction()
     * 
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        this.getNode().fire('game:end');
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.EndGame.addMethods({ 
    
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
gamesoup.library.types.EndGame.addMethods({
    // Helper methods go here...
});