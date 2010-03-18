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
gamesoup.library.types.{{ type.name }} = Class.create(gamesoup.library.types.BaseType);
{% if has_parameters %}
/*****************************************************************************/
/*{{ "Parameters"|center:"74" }}
/*****************************************************************************/
{% if built_ins %}//{{ "BUILT-INS"|center:"74" }}
{% for param in built_ins %}// this._{{ param.name|ljust:"42" }} -- {{ param.interface.name }}
{% endfor %}{% endif %}{% if references %}//{{ "REFERENCES"|center:"74" }}
{% for param in references %}// this._{{ param.name|ljust:"42" }} -- {{ param.interface.name }}
{% endfor %}{% endif %}{% endif %}{% if methods %}
/*****************************************************************************/
/*{{ "Interface Methods"|center:"74" }}
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    {% for method in methods %}
    /*
     * {{ method.signature|ljust:"44" }} -- used in {% for interface in method.used_in.all %}{{ interface.name }}{% if not forloop.last %}, {% endif %}{% endfor %}{% code_doc method 1 %}
     */
    {{ method.name }}: function({% for param in method.parameters.all %}{{ param.name }}{% if not forloop.last %}, {% endif %}{% endfor %}) {
        
    }{% if not forloop.last %},{% endif %}
{% endfor %}});{% endif %}

/*****************************************************************************/
/*{{ "Implementation methods"|center:"74" }}
/*{{ "Do not use outside of this module!"|center:"74" }}
/*****************************************************************************/
gamesoup.library.types.{{ type.name }}.addMethods({
    // Helper methods go here...
});{% endif %}
