/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("website_lazy_load_image.lazy_image_loader", function(require) {
    "use strict";

    var Class = require("web.Class");
    var mixins = require("web.mixins");

    /**
     * Handles lazy loading of images.
     */
    var LazyImageLoader = Class.extend(mixins.EventDispatcherMixin, {
        /**
         * The instance of the jQuery lazy loading plugin.
         *
         * @type {jQuery.lazy}
         */
        plugin: null,

        /**
         * Use this to hook on the onFinishedAll of the lazy loading plugin
         * of a specific instance of LazyImageLoader.
         *
         * @type {jQuery.Deferred}
         */
        allFinished: null,

        /**
         * @class
         * @param {String} selector The selector for the elements to lazy load.
         */
        init: function(selector) {
            mixins.EventDispatcherMixin.init.call(this);
            this.allFinished = $.Deferred();
            this.plugin = $(selector)
                .data("loaded", false)
                .lazy(this._getPluginConfiguration());
        },

        /**
         * Get the settings for the initialization of the lazy loading plugin.
         *
         * @private
         * @returns {Object} Lazy loading plugin settings
         */
        _getPluginConfiguration: function() {
            return {
                afterLoad: this._afterLoad.bind(this),
                beforeLoad: this._beforeLoad.bind(this),
                onError: this._onError.bind(this),
                onFinishedAll: this._onFinishedAll.bind(this),
                chainable: false,
                bind: "event",
            };
        },

        /**
         * Triggered by the beforeLoad event of the lazy loading plugin.
         *
         * @param {DOMElement} el
         * @private
         */
        _beforeLoad: function(el) {
            this.trigger("beforeLoad", el);
        },

        /**
         * Triggered by the afterLoad event of the lazy loading plugin.
         *
         * @param {DOMElement} el
         * @private
         */
        _afterLoad: function(el) {
            this.trigger("afterLoad", el);
        },

        /**
         * Triggered by the onError event of the lazy loading plugin.
         *
         * @param {DOMElement} el
         * @private
         */
        _onError: function(el) {
            this.trigger("onError", el);
        },

        /**
         * Triggered by the onFinished event of the lazy loading plugin.
         *
         * @private
         */
        _onFinishedAll: function() {
            this.allFinished.resolve();
            this.trigger("onFinishedAll");
        },
    });

    require("web.dom_ready");
    var lazy_image_loader = new LazyImageLoader(
        "#wrapwrap > main img:not(.lazyload-disable), " +
            "#wrapwrap > footer img:not(.lazyload-disable), " +
            "#wrapwrap > main .lazyload-bg:not(.lazyload-disable)"
    );

    return {
        lazy_image_loader: lazy_image_loader,
        LazyImageLoader: LazyImageLoader,
    };
});
