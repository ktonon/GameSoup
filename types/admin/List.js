/*
 * Type: List
 * A vertical sequence of items that can be updated during the game.
 */
gamesoup.library.types.List = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.List.addMethods({
    
    /*
     * Any dequeue()                                -- used in Queue
     */
    dequeue: function() {
        
    },

    /*
     * Nothing each(Function visitor)               -- used in Iterable
     */
    each: function(visitor) {
        
    },

    /*
     * Nothing enqueue(Any object)                  -- used in Queue
     * Adds an item to the end of an ordered collection.
     * Like standing in line.
     */
    enqueue: function(object) {
        
    },

    /*
     * Any pop()                                    -- used in Stack
     */
    pop: function() {
        
    },

    /*
     * Nothing push(Any object)                     -- used in Stack
     */
    push: function(object) {
        
    },

    /*
     * Nothing receive(Any object)                  -- used in Receiver
     */
    receive: function(object) {
        
    },

    /*
     * Nothing render()                             -- used in Renderable
     */
    render: function() {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.List.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */
    render: function() {
        // this._node has already been created by this point
        this._node.insert({bottom: '<ul class="box list inner-container"></ul>'});
        this._listNode = this._node.down('.list');
    },
    
    stateSchema: function() {
        
    },
    
    initialState: function() {
        
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
gamesoup.library.types.List.addMethods({
    // Helper methods go here...
});