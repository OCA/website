/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_snippet_timeline.editor', function (require) {
    'use strict';

    var options = require('web_editor.snippets.options');

    options.registry.timeline_item = options.Class.extend({

        /**
         * @override
         */
        onFocus: function () {
            this.trigger_up('option_update', {
                optionNames: ['o_animate'],
                name: 'target',
                data: this.$target.find('.timeline-panel'),
            });
        },
    });
});
