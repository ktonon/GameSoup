/*
 * Type: BoggleWordScoring
 * A mutator that takes a word and computes a boggle score.
 */
gamesoup.library.types.BoggleWordScoring = Class.create(gamesoup.library.types.BaseType);

/*****************************************************************************/
/*                             Interface Methods                             */
/*****************************************************************************/
gamesoup.library.types.BoggleWordScoring.addMethods({
    
    /*---------------------------------------->                         Mutator
     * mutate(x : []) : Integer!
     * 
     * Mutate objects of type domain into objects of type range.
     */                                                               /* vVv */
    mutate: function(x) {
        switch(x.length) {
            case 3:
            case 4:
                return 1;
            case 5:
                return 2;
            case 6:
                return 3;
            case 7:
                return 5;
            default:
                return x.length > 7 ? 11 : 0;
        }
    }                                                                 /* ^A^ */

});

/*****************************************************************************/
/*                                Engine Hooks                               */
/*           These methods are called by the gamesoup match engine.          */
/*                         Do not call them yourself!                        */
/*                    They are called in the order shown.                    */
/*****************************************************************************/
gamesoup.library.types.BoggleWordScoring.addMethods({ 
    
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
gamesoup.library.types.BoggleWordScoring.addMethods({
    // Helper methods go here...
});