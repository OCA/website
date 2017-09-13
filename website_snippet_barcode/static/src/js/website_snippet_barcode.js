/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define('website_snippet_barcode', function (require) {
    "use strict";

    var animation = require('web_editor.snippets.animation');

    animation.registry.barcode = animation.Class.extend({
        selector: '.s_barcode',

        defaults: {
            type: 'QR',
            value: encodeURIComponent(window.location.href),
            aspectratio: '1',
            width: '500',
            humanreadable: 'false'
        },

        start: function () {
            this.defaults.width = this.$target.width();
            this.renderBarcode();
            return this._super();
        },

        renderBarcode: function () {
            var options = _.defaults(this._getOptions(this.$target), this.defaults);
            var height = Math.round(options.width / options.aspectratio);
            var barcodeSrc = '/report/barcode?type=' + options.type +
                             '&value=' + options.value +
                             '&width=' + options.width +
                             '&height=' + height +
                             '&humanreadable=' + Number(options.humanreadable === 'true');

            this.$target.find('img').attr('src', barcodeSrc);
            _.each(options, $.proxy(this._setDataAttribute, this));
            // Set height to ensure proper editor overlay sizing
            this.$target.height(height);
        },

        _getOptions: function ($target) {
            return Object.keys(this.defaults).reduce(function (obj, key) {
                obj[key] = $target.attr('data-' + key);
                return obj;
            }, {});
        },

        _setDataAttribute: function (value, key) {
            this.$target.attr('data-' + key, value);
        }

    });

    return {Barcode: animation.registry.barcode};

});
