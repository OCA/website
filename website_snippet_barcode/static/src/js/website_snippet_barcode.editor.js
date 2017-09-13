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
            this._handleResize();
            return this._super();
        },

        select_aspectratio: function (type, value) {
            this._setOption('aspectratio', Number(value));
        },

        select_humanreadable: function (type) {
            var toggled = String(!(this._getValue('humanreadable') === 'true'));
            this._setOption('humanreadable', toggled);
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
            var dataOptions = ['type', 'value', 'aspectratio', 'humanreadable'];
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

        _handleResize: function () {
            // Image is re-rendered on mouseup, but the mousedown event handler
            // is needed if the mouseup occurs outside the resize handle element
            this.$overlay.find(".oe_handle:not(.size), .oe_handle.size .size").on(
                'mousedown',
                $.proxy(function () {
                    // Remove height for better-looking editor resizing
                    this.$target.css('height', '');
                    $(document).on('mouseup.barcodeHandle', $.proxy(function () {
                        this._setImageSize();
                        $(document).off('.barcodeHandle');
                    }, this));
                }, this)
            );
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
            ).addBack().not('.dropdown-submenu').removeClass("active").filter(
                '[data-' + dataKey + '="' + active + '"]'
            ).addClass("active");
        },

        _setImageSize: function () {
            this._setOption('width', this.$target.width());
        },

        _setOption: function (option, value) {
            this.$target.attr('data-' + option, value);
            this.$target.data('snippet-view').renderBarcode();
        }

    });

});
