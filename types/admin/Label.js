/*
 * Type: Label
 * A simple way to place text on the screen. The value never changes throughout the game.
 */
gamesoup.library.types.Label = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._value                                                          String!

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.Label.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        t = new Template('<div class="label" style="font-size: #{size}px">#{value}</div>');
        var s = (this._width / this._value.length * 1.5).round();
        s = s > this._height / 2 ? (this._height / 2).round() : s;
        this._node.insert({bottom: t.evaluate({value: this._value, size: s})});
    },                                                                /* ^A^ */
    
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
gamesoup.library.types.Label.addMethods({
    // Helper methods go here...
});