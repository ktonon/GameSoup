(function() {
gamesoup.namespace('gamesoup.utils');

// Aliases for internal use
var gs = gamesoup;
var mod = gamesoup.utils;
    
// For tracing method calls
mod.Tracer = Class.create({
    initialize: function(options) {
        options = options || {};
        this.indentLevel = 0;
        this.tabSize = options.tabSize || 4;
        this.traceCategories = options.traceCategories || [];
    },
    trace: function(category, message) {
        var categories = category.split(' ');
        var common = categories.intersect(this.traceCategories);
        if (common.length > 0) {
            var args = $A(arguments).slice(2);
            console.log(' '.times(this.indentLevel), common.first() + ': ' + message, args.length > 0 ? args : '');
        }        
    },
    traceMethodCall: function(className, instance, methodName, originalArguments) {
        if (this.traceCategories.member('method')) {
            console.log(
                ' '.times(this.indentLevel),
                className + '.' + methodName,
                originalArguments,
                'instance=>', instance);
        }
    },
    adjustIndent: function(value) {
        this.indentLevel += value;
    },
    tracerize: function(className, klass) {
        // Only traces instance methods.
        console.log('Trazerizing: ', className, klass)
        var attributeNames = $H(klass.prototype).keys();
        for (var i = 0; i < attributeNames.length; i++) {
            var attributeName = attributeNames[i];
            var item = klass.prototype[attributeName];
            if (Object.isFunction(item)) {
                var wrapper = this.makeMethodWrapper(item, className, attributeName);
                klass.prototype[attributeName] = wrapper;
            }
        }
    },
    makeMethodWrapper: function(item, className, methodName) {
        var curried = {
            tracer: this,
            className: className,
            methodName: methodName
        };
        return item.wrap(function(callOriginal) {
            var args = $A(arguments).slice(1);
            curried.tracer.traceMethodCall(curried.className, this, curried.methodName, args);
            curried.tracer.adjustIndent(curried.tracer.tabSize);
            var returnValue = callOriginal(
                args[0], // Hack:
                args[1], // In python, would do this:
                args[2], //     original(*args)
                args[3], // Don't know how to do this in JavaScript.
                args[4], // Doing callOriginal.curry(args)() is like
                args[5], //     original(args)
                args[6], // Which is not what I need.
                args[7], // The tracer will break for functions with
                args[8], // argument lists longer than 10 elements.
                args[9]
                );
            curried.tracer.adjustIndent(-curried.tracer.tabSize);
            curried.tracer.trace('methodEnding', curried.methodName, returnValue);
            return returnValue;
        });
    }
});

// Dummies
gs.trace = function() {};
gs.tracerize = function() {};

mod.enableTracer = function() {
    mod.tracer = new mod.Tracer({
        tabSize: 4,
        traceCategories: [
            'method',
            'methodEnding',
            // 'debug',
            // 'event',
            // 'dom',
            'notACategory'
            ]
        });
    gs.trace = mod.tracer.trace.bind(mod.tracer);
    gs.tracerize = mod.tracer.tracerize.bind(mod.tracer);
}

// Globally disable the tracer by commenting this line
// mod.enableTracer();

})();
