/*
 * Type: SquareGrid
 * A regular board with columns and rows. There are *colCount* columns and *rowCount* rows.
 */
gamesoup.library.types.SquareGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                Parameters                                
/*****************************************************************************/
//                                BUILT-INS                                 
// this._colCount                                   -- Integer
// this._rowCount                                   -- Integer

/*****************************************************************************/
/*                            Interface Methods                             
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({
    
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
gamesoup.library.types.SquareGrid.addMethods({
    // Helper methods go here...
});
