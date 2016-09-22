/* © 2016-TODAY LasLabs Inc.
 * Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

(function ($) {
  "use strict";
  openerp.website.snippet.animationRegistry.form_recaptcha
  = openerp.website.snippet.Animation.extend({
    selector: ".o_website_form_recaptcha",
    start: function() {
      var self = this;
      this._super();
      $.ajax({
        url: '/website/recaptcha/',
        method: 'GET',
        success: function(data){
          data = JSON.parse(data);
          self.$target.append($(
            '<div class="g-recaptcha" data-sitekey="' + data.site_key + '"></div>'
          ));
          $.getScript('https://www.google.com/recaptcha/api.js');
        },
      });
    }

  });

})(jQuery);
