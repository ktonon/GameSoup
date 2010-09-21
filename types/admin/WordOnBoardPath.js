/*
 * Type: WordOnBoardPath
 * Give a word, can a sequence of adjacent cells be found on a board where letters on those cells spell out the word?
 */
gamesoup.library.types.WordOnBoardPath = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._board                           [Board<cell=[Readable<item=String!>]>]
// this._word                                          [Readable<item=String!>]


/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    
    /*---------------------------------------->                       Predicate
     * call() : Boolean!
     * 
     * What is the truth value of this predicate object?
     */                                                               /* vVv */
    call: function() {
        var word = this._word.read();
        if (word.length == 0) {
            this._lastReason = "Please type your word in.";
            return false;
        }
        var solutions = this._getSolutions(word);
        var status = solutions.length != 0;
        if(status) {
            this._board.highlightPath(solutions[0]);
        }
        this._lastReason = (status ? this._successReason : this._failReason).evaluate({word: word});
        return status;
    },                                                                /* ^A^ */

    /*---------------------------------------->                       Predicate
     * reason() : String!
     * 
     * What was the reason for the last answer this predicate gave?
     */                                                               /* vVv */
    reason: function() {
        return this._lastReason;
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._failReason = new Template("The word '#{word}' was not on the board");
        this._successReason = new Template("The word '#{word}' was found!");
        this._lastReason = "";
    }                                                                 /* ^A^ */
    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.WordOnBoardPath.addMethods({
    // Get 
    _getSolutions: function(word) {
        var firstLetterPattern = new RegExp(word[0], 'i');
        var cells = this._board.cells();
        var candidatePaths = cells.findAll(function(cell) {
            return firstLetterPattern.match(cell.read());
        }).collect(function(candidateCell) {
            return $A([candidateCell]);
        });
        
        // Process rest of the word
        for(var i=1; i<word.length; i++) {
            var newCandidatePaths = $A();
            var nextLetterPattern = new RegExp(word[i], 'i');
            for(var j=0; j<candidatePaths.length; j++) {
                var candidatePath = candidatePaths[j];
                var lastCell = candidatePath.last();
                var cells = this._board.cells();
                for(var k=0; k<cells.length; k++) {
                    var cell = cells[k];
                    if( this._board.areAdjacent(lastCell, cell) &&
                        !candidatePath.member(cell) && 
                        nextLetterPattern.match(cell.read())
                        ) {
                        var newPath = candidatePath.clone();
                        newPath.push(cell);
                        newCandidatePaths.push(newPath);
                    }
                }
            }
            candidatePaths = newCandidatePaths;
            if(candidatePaths.length == 0) break;
        }
        return candidatePaths;
    }
});