/*
 * Type: SquareGrid
 * A board arranged in rows and columns.
 */
gamesoup.library.types.SquareGrid = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 BUILT-INS                                 
// this._colCount                                                      Integer!
// this._rowCount                                                      Integer!
//                                 FACTORIES                                 
// this._cellType                       [Readable<item=[]> + Writable<item=[]>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({
    
    /*---------------------------------------->                           Board
     * areAdjacent(a : [] ; b : []) : Boolean!
     * 
     * Are a and b adjacent?
     */                                                               /* vVv */
    areAdjacent: function(a, b) {
        var pa = this._cellPosition(a);
        var pb = this._cellPosition(b);
        var r = (pa.row - pb.row).abs();
        var c = (pa.col - pb.col).abs();
        return r <= 1 && c <= 1 && !(r == 0 && c == 0);
    },                                                                /* ^A^ */

    /*---------------------------------------->                           Board
     * cells() : Array!
     * 
     * An array where each element in the array is of type Board.cell
     */                                                               /* vVv */
    cells: function() {
        return this._cells.clone();
    },                                                                /* ^A^ */

    /*---------------------------------------->                           Board
     * highlightPath(path : Array!)
     * 
     * Given an array of cells that form a path on the board, briefly highlights the cells in the path.
     */                                                               /* vVv */
    highlightPath: function(path) {
        if(this._clearHighlight) this._clearHighlight();
        if(path) {
            path.each(function(cell) {cell.getNode().up('.cell').addClassName('highlight')});      
            this._clearHighlight = function() {
                this._cells.each(function(cell) {cell.getNode().up('.cell').removeClassName('highlight')});
                clearTimeout(this._clearHighlightTimeout);
                this._clearHighlightTimeout = null;
                this._clearHighlight = null;
            };
            this._clearHighlightTimeout = setTimeout(this._clearHighlight.bind(this), 1000);
        }
    },                                                                /* ^A^ */

    /*---------------------------------------->                        Iterable
     * nextInIteration() : [Readable<item=[]> + Writable<item=[]>]
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
        this._createCells();
        this.resetIteration();
    },                                                                /* ^A^ */

    /*
     * Perform custom take-down.
     */                                                               /* vVv */
    unregister: function() {
        
    }                                                                 /* ^A^ */    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.SquareGrid.addMethods({
    _createCells: function() {
        this._cells = $A();
        var selectorTemplate = new Template('.col-#{i}.row-#{j}');
        var cellIDTemplate = new Template('#{id}-cell-#{i}-#{j}');
        var c = {id: this._id};
        for (c.i=0; c.i<this._colCount; c.i++) {
            for (c.j=0; c.j<this._rowCount; c.j++) {
                var cellContainerNode = this._node.down(selectorTemplate.evaluate(c));
                var cell = this._instantiateCell(cellIDTemplate.evaluate(c));
                cellContainerNode.insert({bottom: cell.getNode()});
                this._cells.push(cell);
            }
        }        
    },
    _instantiateCell: function(cellID) {
        var cell = new this._cellType(cellID);
        cell.createDOM();
        if (cell.isVisible()) {
            cell.render();            
        }
        cell.register();
        return cell;        
    },
    _cellPosition: function(cell) {
        var m = /^(?:.+?)-cell-(\d+)-(\d+)$/(cell.getIdentifier());
        return {
            col: new Number(m[1]),
            row: new Number(m[2])
            };
    }
});