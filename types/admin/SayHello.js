/*
 * Type: SayHello
 * A simple object that just opens an alert box with a message. This object is useful during game design as a simple test that an action is getting triggered.
 */
gamesoup.library.types.SayHello = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._message                                    -- String


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.SayHello.addMethods({
    
    /*
     * Nothing call()                               -- used in Action
     * Performs this default action of it's object.
     */
    call: function() {
        alert(this._message);
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.SayHello.addMethods({ 
    
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
gamesoup.library.types.SayHello.addMethods({
    // Helper methods go here...
});