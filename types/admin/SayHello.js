/*
 * Type: SayHello
 * A simple object that just opens an alert box with a message. This object is useful during game design as a simple test that an action is getting triggered.
 */
gamesoup.library.types.SayHello = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._message                                                        String!

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.SayHello.addMethods({
    
    /*---------------------------------------->                          Action
     * doAction()
     * 
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        alert(this._message);
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.SayHello.addMethods({ 
    
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
gamesoup.library.types.SayHello.addMethods({
    // Helper methods go here...
});