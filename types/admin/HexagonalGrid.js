/*
 * Type: HexagonalGrid
 * A board in which each cell is shaped like a hexagon.
 */
gamesoup.library.types.HexagonalGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._radius                                                         Integer
//                                 FACTORIES                                 
// this._cellType                   [Readable<item=item> + Writable<item=item>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({
    
    /*---------------------------------------->                           Board
     * areAdjacent(a : Any ; b : Any) : Boolean
     * 
     * Are a and b adjacent?
     */                                                               /* vVv */
    areAdjacent: function(a, b) {
        
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * nextInIteration() : Any
     * 
     * Get the next object in the sequence. When the sequence is over, this should return null.
     */                                                               /* vVv */
    nextInIteration: function() {
        
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * resetIteration()
     * 
     * Reset the iteraction. The next call to nextInIteration should be the first in the sequence.
     */                                                               /* vVv */
    resetIteration: function() {
        
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
        
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
        
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({
    // Helper methods go here...
});