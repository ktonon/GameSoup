/*
 * Type: SquareGrid
 * A regular board with columns and rows. There are *colCount* columns and *rowCount* rows.
 */
gamesoup.library.types.SquareGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._colCount                                   -- Integer
// this._rowCount                                   -- Integer


/*****************************************************************************/
/*                             Interface Methods                             */
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
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */
    render: function() {
        // this._node has already been created by this point
        this._node.insert({bottom: '<div class="inner-container"></div>'});
        var container = this._node.down('.inner-container');
        var t = new Template('<div class="col-#{i} row-#{j} cell" style="position: absolute; left: #{left}px; top: #{top}px; width: #{width}px; height: #{height}px;"></div>')
        var c = {
            left: 0,
            top: 0,
            width: (this._width / this._colCount).round() - 2,
            height: (this._height / this._rowCount).round() - 2
        };
        for (c.i=0; c.i<this._colCount; c.i++) {
            c.top = 0;
            for (c.j=0; c.j<this._rowCount; c.j++) {
                container.insert({bottom: t.evaluate(c)});
                c.top += c.height + 2;
            }
            c.left += c.width + 2;
        }
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
gamesoup.library.types.SquareGrid.addMethods({
    // Helper methods go here...
});