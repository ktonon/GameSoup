/*
 * Type: List
 * A vertical sequence of items that can be updated during the game.
 */
gamesoup.library.types.List = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                            Interface Methods                             
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
/*                          Implementation methods                          
/*                    Do not use outside of this module!                    
/*****************************************************************************/
gamesoup.library.types.List.addMethods({
    // Helper methods go here...
});
