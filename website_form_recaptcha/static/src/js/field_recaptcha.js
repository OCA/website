/* Copyright 2016-2017 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_form_recaptcha.recaptcha', function(require){
    "use strict";

    var ajax = require('web.ajax');
    var snippet_animation = require('website.content.snippets.animation');

    snippet_animation.registry.form_builder_send = snippet_animation.registry.form_builder_send.extend({

        start: function() {
            var self = this;
            this._super();
            this.$captchas = self.$('.o_website_form_recaptcha');
            ajax.post('/website/recaptcha/', {}).then(
                function (result) {
                    var data = JSON.parse(result);
                    self.$captchas.append($(
                        '<div class="g-recaptcha" data-sitekey="' + data.site_key + '"></div>'
                    ));
                    if (self.$captchas.length) {
                        $.getScript('https://www.google.com/recaptcha/api.js');
                    }
                }
            );
        }
    });
});
