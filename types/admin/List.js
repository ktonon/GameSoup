/*
 * Type: List
 * A vertical sequence of items that can be updated during the game.
 */
gamesoup.library.types.List = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.List.addMethods({
    
    /*---------------------------------------->                        Iterable
     * nextInIteration() : []
     * 
     * Get the next object in the sequence. When the sequence is over, this should return null.
     */                                                               /* vVv */
    nextInIteration: function() {
        var item = this._items[this._iteratorIndex];
        this._iteratorIndex++;
        return item;
    },                                                                /* ^A^ */

    /*---------------------------------------->                           Stack
     * pop() : []
     * 
     * Remove the object at the top of the stack and return it.
     */                                                               /* vVv */
    pop: function() {
        this._listNode.select('li').first().remove();
        return this._items.pop();
    },                                                                /* ^A^ */

    /*---------------------------------------->                           Stack
     * push(item : [])
     * 
     * Push an object on top of the stack.
     */                                                               /* vVv */
    push: function(item) {
        this._listNode.insert(this._listItemTemplate.evaluate({item: item}));
        this._items.push(item);
        this._node.fire('gs:changed');
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Readable
     * read() : []
     * 
     * Read this content of this object.
     */                                                               /* vVv */
    read: function() {
        return this._items.first();
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * resetIteration()
     * 
     * Reset the iteraction. The next call to nextInIteration should be the first in the sequence.
     */                                                               /* vVv */
    resetIteration: function() {
        this._iteratorIndex = 0;
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Writable
     * write(item : [])
     * 
     * Write a value to the content of this object.
     */                                                               /* vVv */
    write: function(item) {
        this.push(item);
        this._node.fire('gs:changed');
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.List.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        this._node.insert({bottom: '<ul class="box list inner-container"></ul>'});
        this._listNode = this._node.down('.list');
    },                                                                /* ^A^ */
    
    /*
     *
     */                                                               /* vVv */
    stateSchema: function() {
        
    },                                                                /* ^A^ */
    
    /*
     *
     */                                                               /* vVv */
    initialState: function() {
        
    },                                                                /* ^A^ */
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._listItemTemplate = new Template('<li>#{item}</li>');
        this._items = $A();
        this.resetIteration();
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.List.addMethods({
    // Helper methods go here...
});