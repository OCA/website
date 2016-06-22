/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');
  var Model = require('web.Model');

  snippet_animation.registry.field_autocomplete = snippet_animation.Class.extend({

    selector: '.js_website_autocomplete',

    /* Query remote server for autocomplete suggestions
     * @param request object Request from jQueryUI Autocomplete
     * @param response function Callback for response, accepts array of str
     */
    autocomplete: function(self, request, response) {
      var QueryModel = new Model(self.$target.data('model'));
      var queryField = self.$target.data('query-field') || 'name';
      var displayField = self.$target.data('display-field') || queryField;
      var limit = self.$target.data('limit') || 10;
      var domain = [[queryField, 'ilike', request.term]];
      var add_domain = self.$target.data('domain');
      if (add_domain) {
        domain = domain.concat(add_domain);
      }
      QueryModel.call('search_read', [domain, [displayField]], {limit: limit})
        .then(function(records) {
          var data = records.reduce(function(a, b) {
            a.push(b[displayField]);
            return a;
          }, []);
          response(data);
        });
    },
    
    start: function() {
      var self = this;
      this.$target.autocomplete({
        source: function(request, response) {
          self.autocomplete(self, request, response);
        },
      });
    },
    
  });
    
  return {field_autocomplete: snippet_animation.registry.field_autocomplete};

});
