/*
 * Type: TextInput
 * For entering text.
 */
gamesoup.library.types.TextInput = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.TextInput.addMethods({
    
    /*
     * String read()                                -- used in ReadWrite, Readable
     */
    read: function() {
        
    },

    /*
     * Nothing write(String w)                      -- used in ReadWrite, Writable
     */
    write: function(w) {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.TextInput.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */
    render: function() {
        // this._node has already been created by this point
        t = new Template('<input type="text" style="width: 100%; height: 100%; font-size: #{size}px" />');
        var s = (this._height / 2).round();
        this._node.insert({bottom: t.evaluate({size: s})});
    },
    
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
gamesoup.library.types.TextInput.addMethods({
    // Helper methods go here...
});