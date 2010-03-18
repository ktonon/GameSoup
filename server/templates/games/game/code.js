{% load games library %}/*
 * Game: {{ game.name }}{% code_doc game %}
 */

/*===============================================================================================*/
/*{{ "Types"|center:"95" }}*/
/*===============================================================================================*/
{% for type in types %}
/*...............................................................................................*/
/*{{ type.name|center:"95"}}*/ (function () {
{{ type.code }}{% if type.visible %}
gamesoup.library.types.{{ type.name }}.addMethods(gamesoup.library.mixins.Visible);{% endif %}{% if type.has_state %}
gamesoup.library.types.{{ type.name }}.addMethods(gamesoup.library.mixins.Stateful);{% endif %}

})(); // End of {{ type.name }}


{% endfor %}

/*===============================================================================================*/
/*{{ "Instantiate Objects"|center:"95" }}*/
/*===============================================================================================*/

gamesoup.matches.objects = {};
{% for obj in objects %}gamesoup.matches.objects[{{ obj.id }}] = new gamesoup.library.types.{{ obj.type.name|ljust:"40" }}();
{% endfor %}


/*===============================================================================================*/
/*{{ "Configure objects"|center:"95" }}*/
/*===============================================================================================*/

{% for obj in objects %}
/*...............................................................................................*/
/*{{ obj|center:"95" }}*/

{% set_object_parameters obj %}{% if obj.per_player %}gamesoup.matches.objects[{{ obj.id }}].setStatePerPlayer();
{% endif %}{% if obj.type.visible %}gamesoup.matches.objects[{{ obj.id }}].setPosition({{ obj.x }}, {{ obj.y }});
gamesoup.matches.objects[{{ obj.id }}].setSize({{ obj.width }}, {{ obj.height }});
{% endif %}

{% endfor %}
