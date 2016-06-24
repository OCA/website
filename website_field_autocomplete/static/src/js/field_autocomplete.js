/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');
  var $ = require('$');

  snippet_animation.registry.field_autocomplete = snippet_animation.Class.extend({

    selector: '.js_website_autocomplete',

    /* Query remote server for autocomplete suggestions
     * @param request object Request from jQueryUI Autocomplete
     * @param response function Callback for response, accepts array of str
     */
    autocomplete: function(request, response) {
      var self = this;
      var domain = [[this.queryField, 'ilike', request.term]];
      if (this.add_domain) {
        domain = domain.concat(this.add_domain);
      }
      return $.ajax({
        url: '/website/field_autocomplete/' + self.model,
        method: 'GET',
        data: {
          domain: JSON.stringify(domain),
          fields: JSON.stringify(self.fields),
          limit: self.limit,
        },
      }).then(function(records) {
          var data = JSON.parse(records).reduce(function(a, b) {
            a.push(b[self.displayField]);
            return a;
          }, []);
          response(data);
        });
    },
    
    start: function() {
      var self = this;
      this.model = this.$target.data('model');
      this.queryField = this.$target.data('query-field') || 'name';
      this.displayField = this.$target.data('display-field') || this.queryField;
      this.limit = this.$target.data('limit') || 10;
      this.add_domain = this.$target.data('domain');
      this.fields = [this.displayField];
      this.$target.autocomplete({
        source: function(request, response) {
          self.autocomplete(request, response);
        },
      });
    },
    
  });
    
  return {field_autocomplete: snippet_animation.registry.field_autocomplete};

});
