{% load library %}{% if type.is_conflicted %}/*
 * Type: {{ type.name }}
 *
 * YOUR TYPE IS CONFLICTED!!!
 *
 * THESE METHOD CONFLICT:
{% for method in type.conflicting_methods %} *     {{ method.signature|ljust:"44" }} -- used in {{ method.interface.name }}
{% endfor %} */
{% else %}/*
 * Type: {{ type.name}}{% code_doc type %}
 */
gamesoup.library.types.{{ type.name }} = Class.create(gamesoup.library.types.BaseType);{% if has_parameters %}

/*****************************************************************************/
/*{{ "Parameters"|center:"75" }}*/
/*****************************************************************************/{% if built_ins %}
//{{ "BUILT-INS"|center:"75" }}{% for param in built_ins %}
// this._{{ param.name|ljust:"25" }} {{ param.expression|safe|rjust:"44" }}{% endfor %}{% endif %}{% if references %}
//{{ "REFERENCES"|center:"75" }}
{% for param in references %}// this._{{ param.name|ljust:"25" }} {{ param.expression|safe|rjust:"44" }}
{% endfor %}{% endif %}{% endif %}{% if factories %}
//{{ "FACTORIES"|center:"75" }}
{% for factory in factories %}// this._{{ factory.name|ljust:"25" }} {{ factory.expression|safe|rjust:"44" }}
{% endfor %}{% endif %}{% if methods %}

/*****************************************************************************/
/*{{ "Interface Methods"|center:"75" }}*/
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    {% for method in methods %}
    /*---------------------------------------->{{ method.interface.name|rjust:"32" }}
     * {{ method.signature }}
     * {% code_doc method 1 %}
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
        {% engine_hook parsed "render" %}
    },{{ "/* ^A^ */"|rjust:"73" }}{% endif %}{% if type.has_state %}
    
    /*
     *
     */{{ "/* vVv */"|rjust:"72" }}
    stateSchema: function() {
        {% engine_hook parsed "stateSchema" %}
    },{{ "/* ^A^ */"|rjust:"73" }}
    
    /*
     *
     */{{ "/* vVv */"|rjust:"72" }}
    initialState: function() {
        {% engine_hook parsed "initialState" %}
    },{{ "/* ^A^ */"|rjust:"73" }}{% endif %}
    
    /*
     * Perform custom initialization.
     */{{ "/* vVv */"|rjust:"72" }}
    register: function() {
        {% engine_hook parsed "register" %}
    } {{ "/* ^A^ */"|rjust:"73" }}
    
});

/*****************************************************************************/
/*{{ "Implementation Methods"|center:"75" }}*/
/*{{ "Do not use outside of this module!"|center:"75" }}*/
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    {% if parsed.implementation %}{{ parsed.implementation }}{% else %}// Helper methods go here...{% endif %}
});{% endif %}