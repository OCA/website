/* global Typed*/
odoo.define("website_typed_text.frontend", function(require) {
    "use strict";

    var snippetAnimation = require("website.content.snippets.animation");

    var AnimatedTextMixin = {
        _fetchSettingsFromElement: function($el) {
            var data = $el.data();
            var settings = {
                strings: [],
                typeSpeed: data.typeSpeed,
                loop: data.loop === 1,
                backSpeed: data.backSpeed,
                backDelay: data.backDelay,
                cursorChar: data.cursorChar,
                showCursor: data.cursorChar.length > 0,
                smartBackspace: true,
            };
            _.each(data, function(value, key) {
                if (_.str.startsWith(key, "strings-") && value) {
                    settings.strings.push(value);
                }
            });
            return settings;
        },
    };

    snippetAnimation.registry.typed_text = snippetAnimation.Animation.extend(
        AnimatedTextMixin,
        {
            selector: ".typed_text",
            disabledInEditableMode: true,
            start: function() {
                var res = this._super.apply(this, arguments);

                var data = this.$target.data();
                var strings = [];
                _.each(data, function(value, key) {
                    if (_.str.startsWith(key, "strings-")) {
                        strings.push(value);
                    }
                });
                this.$target.attr("data-original", this.$target.text());
                this.$target.attr("data-css-height", this.$target[0].style.height);
                this.$target.height(this.$target.height());
                this.$target.text("");
                var settings = this._fetchSettingsFromElement(this.$target);
                this.typed = new Typed(this.$target[0], settings);
                return res;
            },

            destroy: function() {
                var res = this._super.apply(this, arguments);
                this.typed.destroy();
                this.$target.css("height", this.$target.attr("data-css-height"));
                this.$target.text(this.$target.attr("data-original"));
                return res;
            },
        }
    );

    return {
        AnimatedTextMixin: AnimatedTextMixin,
    };
});
