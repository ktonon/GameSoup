/*
 * Type: SquareGrid
 * A board arranged in rows and columns.
 */
gamesoup.library.types.SquareGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._colCount                                                       Integer
// this._rowCount                                                       Integer

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({
    
    /*---------------------------------------->                           Board
     * areAdjacent(a : Item ; b : Item) : Boolean
     * 
     * Are a and b adjacent?
     */                                                               /* vVv */
    areAdjacent: function(a, b) {
        
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * nextInIteration() : Item
     * 
     * Get the next object in the sequence. When the sequence is over, this should return null.
     */                                                               /* vVv */
    nextInIteration: function() {
        var cell = this._cells[this._iteratorIndex];
        this._iteratorIndex++;
        return cell;
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * resetIteration()
     * 
     * Reset the iteraction. The next call to nextInIteration should be the first in the sequence.
     */                                                               /* vVv */
    resetIteration: function() {
        this._iteratorIndex = 0;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({ 
    
    /*
     * Extend the DOM and apply styling.
     */                                                               /* vVv */
    render: function() {
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
        this._cells = $A();
        this._factory = new gamesoup.library.types.CellFactory();
        var t = new Template('.col-#{i}.row-#{j}');
        var c = {};
        for (c.i=0; c.i<this._colCount; c.i++) {
            for (c.j=0; c.j<this._rowCount; c.j++) {
                var cell = this._factory.instantiate();
                var cellContainerNode = this._node.down(t.evaluate(c));
                cellContainerNode.insert({bottom: cell._node});
                this._cells.push(cell);
            }
        }
        this.resetIteration();
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({
    // Helper methods go here...
});