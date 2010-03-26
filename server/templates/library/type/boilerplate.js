{% load library %}{% if type.is_conflicted %}/*
 * Type: {{ type.name }}
 *
 * YOUR TYPE IS CONFLICTED!!!
 *
 * THESE METHOD CONFLICT:
{% for method in type.conflicting_methods %} *     {{ method.signature|ljust:"44" }} -- used in {{ method.used_in_short }}
{% endfor %} */
{% else %}/*
 * Type: {{ type.name}}{% code_doc type %}
 */
gamesoup.library.types.{{ type.name }} = Class.create(gamesoup.library.types.BaseType);{% if has_parameters %}

/*****************************************************************************/
/*{{ "Parameters"|center:"75" }}*/
/*****************************************************************************/{% if built_ins %}
//{{ "BUILT-INS"|center:"75" }}{% for param in built_ins %}
// this._{{ param.name|ljust:"42" }} -- {{ param.interface.name }}{% endfor %}{% endif %}{% if references %}
//{{ "REFERENCES"|center:"75" }}
{% for param in references %}// this._{{ param.name|ljust:"42" }} -- {{ param.interface.name }}
{% endfor %}{% endif %}{% endif %}{% if methods %}

/*****************************************************************************/
/*{{ "Interface Methods"|center:"75" }}*/
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    {% for method in methods %}
    /*
     * {{ method.signature|ljust:"44" }} -- used in {% for interface in method.used_in.all %}{{ interface.name }}{% if not forloop.last %}, {% endif %}{% endfor %}{% code_doc method 1 %}
     */{{ "/* vVv */"|rjust:"72" }}
    {{ method.name }}: function({% for param in method.parameters.all %}{{ param.name }}{% if not forloop.last %}, {% endif %}{% endfor %}) {
        {% interface_method parsed method.name %}
    }{% if not forloop.last %},{% else %} {% endif %}{{ "/* ^A^ */"|rjust:"73" }}
{% endfor %}
});{% endif %}

/*****************************************************************************/
/*{{ "Engine Hooks"|center:"75" }}*/
/*{{ "These methods are called by the gamesoup match engine."|center:"75"}}*/
/*{{ "Do not call them yourself!"|center:"75" }}*/
/*{{ "They are called in the order shown."|center:"75" }}*/
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({ {% if type.visible %}
    
    /*
     * Extend the DOM and apply styling.
     */{{ "/* vVv */"|rjust:"72" }}
    render: function() {
        {{ parsed|engine_hook:"render" }}
    },{{ "/* ^A^ */"|rjust:"73" }}{% endif %}{% if type.has_state %}
    
    /*
     *
     */{{ "/* vVv */"|rjust:"72" }}
    stateSchema: function() {
        {{ parsed|engine_hook:"stateSchema" }}
    },{{ "/* ^A^ */"|rjust:"73" }}
    
    /*
     *
     */{{ "/* vVv */"|rjust:"72" }}
    initialState: function() {
        {{ parsed|engine_hook:"initialState" }}
    },{{ "/* ^A^ */"|rjust:"73" }}{% endif %}
    
    /*
     * Perform custom initialization.
     */{{ "/* vVv */"|rjust:"72" }}
    register: function() {
        {{ parsed|engine_hook:"register" }}
    } {{ "/* ^A^ */"|rjust:"73" }}
    
});

/*****************************************************************************/
/*{{ "Implementation Methods"|center:"75" }}*/
/*{{ "Do not use outside of this module!"|center:"75" }}*/
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    {% if parsed.implementation %}{{ parsed.implementation }}{% else %}// Helper methods go here...{% endif %}
});{% endif %}