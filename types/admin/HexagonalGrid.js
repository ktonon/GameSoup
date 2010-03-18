/*
 * Type: HexagonalGrid
 * A board in which each cell is shaped like a hexagon.
 */
gamesoup.library.types.HexagonalGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                Parameters                                
/*****************************************************************************/
//                                BUILT-INS                                 
// this._radius                                     -- Integer

/*****************************************************************************/
/*                            Interface Methods                             
/*****************************************************************************/
gamesoup.library.types.HexagonalGrid.addMethods({
    
    /*
     * Iterable adjacentTo(Cell a)                  -- used in Board
     */
    adjacentTo: function(a) {
        
    },

    /*
     * Boolean areAdjacent(Cell a, Cell b)          -- used in Board
     */
    areAdjacent: function(a, b) {
        
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
gamesoup.library.types.HexagonalGrid.addMethods({
    // Helper methods go here...
});
