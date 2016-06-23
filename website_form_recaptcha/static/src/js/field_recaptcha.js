/* © 2016-TODAY LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_form_recaptcha.recaptcha', function(require){
  "use strict";
  
  var snippet_animation = require('web_editor.snippets.animation');
  var $ = require("$");
  
  snippet_animation.registry.form_builder_send = snippet_animation.registry.form_builder_send.extend({
    
    start: function() {
      var self = this;
      this._super();
      this.$captchas = self.$('.o_website_form_recaptcha');
      $.ajax({
        url: '/website/recaptcha/',
        method: 'GET',
        success: function(data){
          data = JSON.parse(data);
          self.$captchas.append($(
            '<div class="g-recaptcha" data-sitekey="' + data.site_key + '"></div>'
          ));
          if (self.$captchas.length) {
            $.getScript('https://www.google.com/recaptcha/api.js');
          }
        },
      });
    }
    
  });
  
});
