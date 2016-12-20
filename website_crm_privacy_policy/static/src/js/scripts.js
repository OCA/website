/**
 * Copyright 2014 Jorge Camacho <jcamacho@trey.es>
 * Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
 * Copyright 2016 Vicent Cubells <vicent.cubells@tecnativa.com>
 */
odoo.define('website_crm_privacy_policy.crm_policy', function (require) {
    'use strict';

    var core = require('web.core');
    var _t = core._t;
    var animation = require('web_editor.snippets.animation');


    return animation.registry.accept_policy = animation.Class.extend({
        selector: '.s_website_form',

        start: function() {
            this.$('.o_website_form_send').on('click', $.proxy(this.accept_policy, this));
        },

        // Validate form
        accept_policy: function(event) {
            event.preventDefault();  // Prevent the default submit behavior

            if(!this.$('input[name="privacy_policy"]').is(':checked')) {
                alert(_t('You must accept our Privacy Policy.'));
            }
        },
    });
});
