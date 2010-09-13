/*
 * Type: EnterKeyPressed
 * Do something when the enter key is pressed and when a given object has focus.
 */
gamesoup.library.types.EnterKeyPressed = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._action                                                        [Action]
// this._focus                                                               []


/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.EnterKeyPressed.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._keyObserver = function(event) {
            if (event.keyCode == Event.KEY_RETURN) {
                this._action.doAction();
            }
        }.bind(this);
        this._focus.observe('keydown', this._keyObserver);
    },                                                                /* ^A^ */

    /*
     * Perform custom take-down.
     */                                                               /* vVv */
    unregister: function() {
        this._focus.stopObserving('keydown', this._keyObserver);
        this._keyObserver = null;
    }                                                                 /* ^A^ */    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.EnterKeyPressed.addMethods({
    // Helper methods go here...
});