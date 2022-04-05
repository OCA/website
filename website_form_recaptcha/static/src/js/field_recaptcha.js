/* Copyright 2016-2017 LasLabs Inc.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define("website_form_recaptcha.recaptcha", function(require) {
    "use strict";

    const ajax = require("web.ajax");
    const core = require("web.core");
    const qweb = core.qweb;
    var publicWidget = require("web.public.widget");

    publicWidget.registry.form_builder_send.include({
        // https://developers.google.com/recaptcha/docs/language
        captcha_languages: [
            "ar",
            "af",
            "am",
            "hy",
            "az",
            "eu",
            "bn",
            "bg",
            "ca",
            "zh-HK",
            "zh-CN",
            "zh-TW",
            "hr",
            "cs",
            "da",
            "nl",
            "en-GB",
            "en",
            "et",
            "fil",
            "fi",
            "fr",
            "fr-CA",
            "gl",
            "ka",
            "de",
            "de-AT",
            "de-CH",
            "el",
            "gu",
            "iw",
            "hi",
            "hu",
            "is",
            "id",
            "it",
            "ja",
            "kn",
            "ko",
            "lo",
            "lv",
            "lt",
            "ms",
            "ml",
            "mr",
            "mn",
            "no",
            "fa",
            "pl",
            "pt",
            "pt-BR",
            "pt-PT",
            "ro",
            "ru",
            "sr",
            "si",
            "sk",
            "sl",
            "es",
            "es-419",
            "sw",
            "sv",
            "ta",
            "te",
            "th",
            "tr",
            "uk",
            "ur",
            "vi",
            "zu",
        ],
        recaptcha_js_url: "https://www.google.com/recaptcha/api.js",
        /**
         * We want to load the recaptcha code dinamically for every form enabled model
         *
         * @override
         */
        start: function() {
            this._super();
            var _this = this;
            const model_name = this.$target.data("model_name");
            if (!model_name) {
                return;
            }
            ajax.post("/website/recaptcha/form_enabled/" + model_name, {}).then(
                function(recaptcha_required) {
                    if (recaptcha_required) {
                        ajax.loadXML(
                            "/website_form_recaptcha/static/src/xml/recaptcha.xml",
                            qweb
                        ).then(function() {
                            // Remove any previous captcha code
                            _this.$target
                                .find(".o_website_form_recaptcha")
                                .closest(".form-group")
                                .remove();
                            _this.$target
                                .find(".form-group:has('.o_website_form_send')")
                                .before(
                                    $(qweb.render("website_form_recaptcha.recaptcha"))
                                );
                            _this.$captchas = _this.$(".o_website_form_recaptcha");
                            _this.handle_captcha();
                        });
                    }
                }
            );
        },
        handle_captcha: function() {
            var self = this;
            return ajax.post("/website/recaptcha/", {}).then(function(result) {
                var data = JSON.parse(result);
                self.$captchas.append(self._get_captcha_elem(data));
                if (self.$captchas.length) {
                    $.getScript(self._get_captcha_script_url(data));
                }
            });
        },
        _get_captcha_elem: function(data) {
            return $("<div/>", {
                class: "g-recaptcha",
                "data-sitekey": data.site_key,
            });
        },
        _get_captcha_script_url: function() {
            var lang = $("html")
                .attr("lang")
                .replace("_", "-");
            if (this.captcha_languages.includes(lang)) {
                // Lookup for specific localization (ie: fr-FR)
                return this.recaptcha_js_url + "?hl=" + lang;
            }
            if (this.captcha_languages.includes(lang.slice(0, 2))) {
                // Fallback to main lang
                return this.recaptcha_js_url + "?hl=" + lang.slice(0, 2);
            }
            // If both failed -> let google pick browser language
            return this.recaptcha_js_url;
        },
    });
});
