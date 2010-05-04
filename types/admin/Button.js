/*
 * Type: Button
 * A simple push button. Connect actions to its "click" event to make it useful.
 */
gamesoup.library.types.Button = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._label                                                          String!
//                                 REFERENCES                                
// this._action                                                        [Action]


/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.Button.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        t = new Template('<input type="button" value="#{label}" style="width: 100%; height: 100%; font-size: #{size}px" />');
        var s = (this._width / this._label.length * 1.5).round();
        s = s > this._height / 2 ? (this._height / 2).round() : s;
        this._node.insert({bottom: t.evaluate({label: this._label, size: s})});
        this._buttonNode = this._node.down('input[type=button]');
    },                                                                /* ^A^ */
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._buttonNode.observe('click', this._action.doAction.bind(this._action));
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.Button.addMethods({
    // Helper methods go here...
});