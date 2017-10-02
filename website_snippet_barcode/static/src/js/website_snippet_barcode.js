/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define('website_snippet_barcode', function (require) {
    "use strict";

    var animation = require('web_editor.snippets.animation');

    animation.registry.barcode = animation.Class.extend({
        selector: '.s_barcode',

        defaults: {
            type: 'QR',
            value: encodeURIComponent(window.location.href.split('#')[0]),
            aspectRatio: '1',
            humanReadable: 'none'
        },

        start: function () {
            this.defaults.width = this.$target.width();
            this.renderBarcode();
            return this._super();
        },

        renderBarcode: function () {
            var options = _.defaults(this._getOptions(), this.defaults);
            var height = Math.round(options.width / options.aspectRatio);
            var humanReadableImage = Number(options.humanReadable === 'image');
            var barcodeSrc = '/report/barcode?type=' + options.type +
                             '&value=' + options.value +
                             '&width=' + options.width +
                             '&height=' + height +
                             '&humanreadable=' + humanReadableImage;

            _.each(options, $.proxy(this._setDataAttribute, this));
            this.$target.find('.o_barcode_img').attr('src', barcodeSrc);
            this._renderFooter(options.humanReadable, options.value);
        },

        _getOptions: function () {
            return _.reduce(Object.keys(this.defaults), function (obj, key) {
                obj[key] = this.$target.attr('data-' + key);
                return obj;
            }, {}, this);
        },

        _renderFooter: function (humanReadable, value) {
            var $footer = this.$target.find('.o_barcode_text');
            if (humanReadable === 'text') {
                $footer.text(decodeURIComponent(value)).removeClass('hidden');
            } else {
                $footer.text('').addClass('hidden');
            }
        },

        _setDataAttribute: function (value, key) {
            this.$target.attr('data-' + key, value);
        }

    });

    return {Barcode: animation.registry.barcode};

});
