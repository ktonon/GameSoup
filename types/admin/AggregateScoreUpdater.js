/*
 * Type: AggregateScoreUpdater
 * Maintains a score field by applying a scoring function to a collection and summing the results.
 */
gamesoup.library.types.AggregateScoreUpdater = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                                 Parameters                                */
/*****************************************************************************/
//                                 REFERENCES                                
// this._scorables                                          [Iterable<item=[]>]
// this._scoreField                                   [Writable<item=Integer!>]
// this._scoreFunction                     [Mutator<domain=[], range=Integer!>]


/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.AggregateScoreUpdater.addMethods({ 
    
    /*
     * Perform custom initialization.
     */                                                               /* vVv */
    register: function() {
        this._scorablesObserver = this.updateScore.bind(this);
        this._scorables.observe('gs:changed', this._scorablesObserver);
    },                                                                /* ^A^ */

    /*
     * Perform custom take-down.
     */                                                               /* vVv */
    unregister: function() {
        this._scorables.stopObserving('gs:changed', this._scorablesObserver);
        this._scorablesObserver = null;
    }                                                                 /* ^A^ */    
});

/*****************************************************************************/
/*                           Implementation Methods                          */
/*                     Do not use outside of this module!                    */
/*****************************************************************************/
gamesoup.library.types.AggregateScoreUpdater.addMethods({
    updateScore: function(event) {
        this._scorables.resetIteration();
        var item;
        var sum = 0;
        while((item = this._scorables.nextInIteration()) != null) {
            sum += this._scoreFunction.mutate(item);
        }
        this._scoreField.write(sum);
    }
});