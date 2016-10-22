/* Copyright 2016 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_field_autocomplete_related.field_autocomplete', function(require){
  "use strict";

  var snippet_animation = require('web_editor.snippets.animation');

  snippet_animation.registry.field_autocomplete = snippet_animation.registry.field_autocomplete.extend({

    $related: false,
    data: {},

    autocomplete: function(request, response) {
      var self = this;
      return this._super(request, response).then(function(records) {
        self.data = {};
        for (var i = 0, len = records.length; i < len; i++) {
          var record = records[i];
          self.data[record.id] = record;
        }
        return records;
      });
    },
    
    /* Update text in related fields
     * @param event Event obj
     * @param ui obj {'value': str, 'label': str}
     */
    autocompleteselect: function(event, ui) {
      event.preventDefault();
      if (!this.$related) {
        return;
      }
      var record = this.data[ui.item.value];
      this.$related.each(function(){
        var $this = $(this);
        var recvField = $this.data('recv-field') || $this.data('query-field') || 'name';
        if (['checkbox', 'radio'].indexOf(this.type) != -1) {
          $(this).attr('checked', record[recvField]);
        } else {
          $(this).val(record[recvField] || '');
        }
      });
    },
    
    start: function() {
      this._super();
      var self = this;
      if (this.valueField != 'id') {
        this.valueField = 'id';
        this.fields.push('id');
      }
      var relationGroup = this.$target.data('relate-send') || this.$target.data('relate-recv');
      if (relationGroup) {
        this.$related = $('*[data-relate-recv="' + relationGroup + '"]')
          .add(this.$target);
        this.$related.each(function() {
          var $this = $(this);
          var field = $this.data('recv-field') || $this.data('query-field');
          if (field){
            self.fields.push(field);
          } 
        });
        this.$target.on('autocompleteselect', function(event, ui) {
          self.autocompleteselect(event, ui);
        });
      }
    },
    
  });

});
