/*
 * Type: HexagonalGrid
 * A board in which each cell is shaped like a hexagon.
 */
gamesoup.library.types.HexagonalGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._radius                                     -- Integer


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({
    
    /*
     * Boolean areAdjacent(Cell a, Cell b)          -- used in Board
     * Are cell a and cell b adjacent?
     */
    areAdjacent: function() {
        
    },

    /*
     * Item nextInIteration()                       -- used in Iterable
     * Get the next object in the sequence. When the sequence is over, this should return null.
     */
    nextInIteration: function() {
        
    },

    /*
     * resetIteration()                             -- used in Iterable
     * Reset the iteraction. The next call to nextInIteration should be the first in the sequence.
     */
    resetIteration: function() {
        
    }

});

/*****************************************************************************/
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */
    render: function() {
        // this._node has already been created by this point
        
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
gamesoup.library.types.HexagonalGrid.addMethods({
    // Helper methods go here...
});