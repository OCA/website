odoo.define("website_typed_text.editor", function(require) {
    "use strict";

    var core = require("web.core");
    var options = require("web_editor.snippets.options");
    var AnimatedTextMixin = require("website_typed_text.frontend").AnimatedTextMixin;
    var Dialog = require("web.Dialog");
    var _t = core._t;
    var qweb = core.qweb;

    options.registry.typed_text = options.Class.extend(AnimatedTextMixin, {
        xmlDependencies: ["/website_typed_text/static/src/xml/editor.xml"],

        start: function() {
            this._super.apply(this, arguments);
            var self = this;
            this.$target.on("snippet-option-change", function() {
                self.onFocus();
            });
        },

        _setActive: function() {
            var res = this._super.apply(this, arguments);
            var $rotationOption = this.$el.find("[data-change-typed-text]");
            $rotationOption.toggleClass("d-none", !this.$target.hasClass("typed_text"));
            return res;
        },

        onFocus: function() {
            var $rotationOption = this.$el.find("[data-change-typed-text]");
            $rotationOption.toggleClass("d-none", !this.$target.hasClass("typed_text"));
        },

        toggleClass: function(previewMode, value) {
            var res = this._super.apply(this, arguments);
            if (value === "typed_text") {
                var $rotationOption = this.$el
                    .parent()
                    .find("[data-change-typed-text]");
                $rotationOption.toggleClass(
                    "d-none",
                    !this.$target.hasClass("typed_text")
                );

                if (this.$target.hasClass("typed_text")) {
                    this._applySettings(this._defaultSettings());
                }
            }
            return res;
        },

        _defaultSettings: function() {
            return {
                strings: [this.$target.text()],
                typeSpeed: 60,
                loop: true,
                backSpeed: 25,
                backDelay: 1500,
                smartBackspace: true,
                cursorChar: "|",
            };
        },

        _fetchSettingsFromTarget: function() {
            return this._fetchSettingsFromElement(this.$target);
        },

        _applySettings: function(settings) {
            this.$target.attr("data-type-speed", settings.typeSpeed);
            this.$target.attr("data-loop", settings.loop ? "1" : "0");
            this.$target.attr("data-back-speed", settings.backSpeed);
            this.$target.attr("data-back-delay", settings.backDelay);
            this.$target.attr("data-cursor-char", settings.cursorChar);

            _.each(
                settings.strings,
                function(string, i) {
                    this.$target.attr(_.str.sprintf("data-strings-%d", i), string);
                }.bind(this)
            );
        },

        changeTypedText: function() {
            var self = this;
            var currentSettings = this._fetchSettingsFromTarget();
            currentSettings.strings = currentSettings.strings.join("\r\n");

            var buttons = [
                {
                    text: _t("Save"),
                    classes: "btn-primary",
                    click: function() {
                        var $strings = this.$("#strings");
                        var $typeSpeed = this.$("#type-speed");
                        var $backSpeed = this.$("#back-speed");
                        var $backDelay = this.$("#back-delay");
                        var $cursorChar = this.$("#cursor-char");
                        var $loop = this.$("#loop");

                        var settings = {
                            strings: $strings.val().split(/\r?\n/),
                            typeSpeed: $typeSpeed.val(),
                            backSpeed: $backSpeed.val(),
                            backDelay: $backDelay.val(),
                            cursorChar: $cursorChar.val(),
                            loop: $loop.is(":checked"),
                        };
                        self._applySettings(settings);
                        this.close();
                    },
                },
                {
                    text: _t("Discard"),
                    close: true,
                },
            ];

            return new Dialog(this, {
                title: _t("Typed Text Animation"),
                $content: $(
                    qweb.render("website_typed_text.Dialog", {
                        currentSettings: currentSettings,
                    })
                ),
                buttons: buttons,
            }).open();
        },
    });
});
