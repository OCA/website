/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete_related.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');

  snippet_animation.registry.field_autocomplete = snippet_animation.registry.field_autocomplete.extend({

    autocomplete: function(request, response) {
      if (this.$target.data('is-tag') !== undefined) {
        request.term = request.term.split( /,\s*/ ).pop();
      }
      return this._super(request, response);
    },
  
    autocompleteArgs: function() {
      var res = this._super();
      if (this.$target.data('is-tag') !== undefined) {
        res.select = function(event, ui) {
          var terms = this.value.split( /,\s*/ );
          terms.pop();
          terms.push(ui.item.value);
          terms.push("");
          this.value = terms.join(', ');
          return false;
        };
        res.focus = function() {
          return false;
        };
      }
      return res;
    },
    
  });
    
  return {field_autocomplete: snippet_animation.registry.field_autocomplete};

});
