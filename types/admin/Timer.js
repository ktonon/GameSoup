/*
 * Type: Timer
 * A simple timer that executes once and calls an action upon completion. The timer will be invisible until it is started (by calling the doAction method), after which point it will display a count-down. The duration is measured in seconds.
 */
gamesoup.library.types.Timer = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._duration                                                      Integer!
//                                 REFERENCES                                
// this._onCompletion                                                  [Action]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.Timer.addMethods({
    
    /*---------------------------------------->                          Action
     * doAction()
     * 
     * Perform the default action of this object.
     */                                                               /* vVv */
    doAction: function() {
        // Start the timer
        this._countDown = this._duration;
        this._tickerNode.innerHTML = this._duration;
        this._timeoutVar = setTimeout(this.timerCompleted.bind(this), this._duration * 1000);
        // For the countdown.
        this._tickerNode.show();
        this._tickerVar = setTimeout(this.updateTicker.bind(this), 1000);
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.Timer.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        var node = this.getNode();
        this._tickerNode = new Element('div', {'class': 'ticker'});
        node.insert({top: this._tickerNode});
        this._tickerNode.hide();
    },                                                                /* ^A^ */
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        
    },                                                                /* ^A^ */

    /*
     * Perform custom take-down.
     */                                                               /* vVv */
    unregister: function() {
        clearTimeout(this._timeoutVar);
        clearTimeout(this._tickerVar);
        this._timeoutVar = null;
        this._tickerVar = null;        
    }                                                                 /* ^A^ */    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.Timer.addMethods({
    timerCompleted: function() {
        this.unregister();
        this._tickerNode.innerHTML = 0;
        this._onCompletion.doAction();
    },
    updateTicker: function() {
        this._countDown -= 1;
        this._tickerNode.innerHTML = this._countDown;
        this._tickerVar = setTimeout(this.updateTicker.bind(this), 1000);
    }
});