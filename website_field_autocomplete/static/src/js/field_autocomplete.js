/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');

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
        dataType: 'json',
        url: '/website/field_autocomplete/' + self.model,
        method: 'GET',
        data: {
          domain: JSON.stringify(domain),
          fields: JSON.stringify(self.fields),
          limit: self.limit,
        },
      }).then(function(records) {
          var data = records.reduce(function(a, b) {
            a.push({label: b[self.displayField], value: b[self.valueField]});
            return a;
          }, []);
          response(data);
          return records;
        });
    },
    
    /* Return arguments that are used to initialize autocomplete */
    autocompleteArgs: function() {
      var self = this;
      return {
        source: function(request, response) {
          self.autocomplete(request, response);
        }
      };
    },
    
    start: function() {
      this.model = this.$target.data('model');
      this.queryField = this.$target.data('query-field') || 'name';
      this.displayField = this.$target.data('display-field') || this.queryField;
      this.valueField = this.$target.data('value-field') || this.displayField;
      this.limit = this.$target.data('limit') || 10;
      this.add_domain = this.$target.data('domain');
      this.fields = [this.displayField];
      if (this.valueField != this.displayField) {
        this.fields.push(this.valueField);
      }
      this.$target.autocomplete(this.autocompleteArgs());
    },
    
  });
    
  return {field_autocomplete: snippet_animation.registry.field_autocomplete};

});
