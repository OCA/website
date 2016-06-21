/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');
  var Model = require('web.Model');

  snippet_animation.registry.field_autocomplete = snippet_animation.Class.extend({

    selector: '.s_website_autocomplete',

    start: function() {

      let self = this;

      this.$target.autocomplete({
        source: function(request, response) {
          // Must use var, let yields undefined
          var QueryModel = new Model(self.$target.data('model'));
          let queryField = self.$target.data('queryField');
          if (!queryField) {
            queryField = 'name';
          }
          let displayField = self.$target.data('displayField');
          if (!displayField) {
            displayField = queryField;
          }
          let limit = self.$target.data('limit');
          if (!limit) {
            limit = 10;
          }
          let domain = [[queryField, 'ilike', request.term]];
          let add_domain = self.$target.data('domain');
          if (add_domain) {
            domain = domain.concat(add_domain);
          }
          QueryModel.call('search_read', [domain, [displayField]], {limit: limit})
            .then(function(records) {
              let data = records.reduce(function(a, b) {
                a.push(b[displayField]);
                return a;
              }, []);
              response(data);
            });
        }
      });
      
    },
    
  });
    
  return {field_autocomplete: snippet_animation.registry.field_autocomplete};

});
