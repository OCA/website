/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define('website_snippet_barcode.editor', function (require) {
    "use strict";

    var options = require('web_editor.snippets.options');
    var website = require("website.website");
    var Barcode = require('website_snippet_barcode').Barcode;

    options.registry.barcode = options.Class.extend({

        start: function () {
            if (!this.$target.data('snippet-view')) {
                this.$target.data('snippet-view', new Barcode(this.$target));
            }
            return this._super();
        },

        select_aspectratio: function (type, value) {
            this._setOption('aspectRatio', value);
        },

        select_humanreadable: function (type, value) {
            this._setOption('humanReadable', value);
        },

        select_type: function (type, value) {
            this._setOption('type', value);
        },

        select_value: function (type, value) {
            if (type !== 'click') {
                return $.Deferred().reject();
            }
            switch(value) {
                case 'current':
                    this._setOption('value', null);
                    break;
                case 'custom':
                    this._promptCustomValue();
                    break;
            }
        },

        set_active: function () {
            var dataOptions = ['type', 'value', 'aspectRatio', 'humanReadable'];
            _.each(dataOptions, $.proxy(this._setActiveOption, this));
        },

        _getValue: function (option) {
            var currentValue = this.$target.attr('data-' + option);
            switch(option) {
                case 'value':
                    return currentValue === this.$target.data('snippet-view').defaults.value
                        ? 'current'
                        : 'custom';
                default:
                    return currentValue;
            }
        },

        _promptCustomValue: function () {
            website.prompt({
                'window_title': 'Custom Barcode Value',
                'input': 'Value',
                "default": decodeURIComponent(this.$target.attr('data-value'))
            }).done($.proxy(function (value) {
                this._setOption('value', encodeURIComponent(value));
            }, this));
        },

        _setActiveOption: function (option) {
            var active = this._getValue(option);
            var dataKey = 'select_'+ option;
            this.$el.find(
                '[data-' + dataKey + ']'
            ).removeClass("active").filter(
                '[data-' + dataKey + '="' + active + '"]'
            ).addClass("active");
        },

        _setOption: function (option, value) {
            this.$target.attr('data-' + option, value);
            this.$target.data('snippet-view').renderBarcode();
        }

    });

});
