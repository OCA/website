/* License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_country_phone_code_dropdown.dropdown", function (require) {
    "use strict";
    const animation = require("website.content.snippets.animation");
    const countryCodeDropdown = animation.registry.website_snippet_country_dropdown;

    const CountryPhoneCodeDropdown = animation.Class.extend({
        selector: ".js_country_phone_code_dropdown",
        start: function () {
            this._super.apply(this, arguments);
            this.prototype = countryCodeDropdown.prototype;
            this.$flag_selector = this.$target.find(".js_select_country_phone_code");
            this.$img_code = this.$target.find(".js_img_country_code");
            this.$btn_country_phone_code = this.$target.find(
                ".js_btn_country_phone_code"
            );
            this.$dropdown_list = this.$target.find("#dropdown-countries");
            this.$country_phone_code_field = this.$target.find(
                ".js_country_phone_code_field"
            );
            this.$no_country_field = this.$target.find(".js_no_country_field");
            this.$complete_field_post = this.$target.find(".js_complete_field_post");
            this.$flag_selector.on("click", $.proxy(this.set_value, this));
            this.$no_country_field.on(
                "change",
                $.proxy(this.on_change_no_country_field, this)
            );
            this.$dropdown_list.on(
                "scroll",
                _.debounce(this.lazy_image_load.bind(this), 35)
            );
            this.$target.on("shown.bs.dropdown", this.lazy_image_load.bind(this));
        },

        set_value: function (event) {
            this.country_phone_code = event.currentTarget.dataset.country_phone_code;
            this.$flag_selector.val(event.currentTarget.id);
            this.$img_code.attr("src", event.currentTarget.dataset.country_image_url);
            this.$btn_country_phone_code.attr(
                "data-country_phone_code",
                event.currentTarget.dataset.country_phone_code
            );
            this.$country_phone_code_field.val(
                "+" + event.currentTarget.dataset.country_phone_code
            );
            $(this.country_phone_code)
                .children()
                .text("+" + String(event.currentTarget.dataset.country_phone_code));
            this.join_value(
                event.currentTarget.dataset.country_phone_code,
                this.$no_country_field.val()
            );
        },
        join_value: function (country_phone_code, value) {
            this.$complete_field_post.val(country_phone_code.concat(" " + value));
        },
        on_change_no_country_field: function () {
            return this.join_value(
                this.$country_phone_code_field.val(),
                this.$no_country_field.val()
            );
        },

        is_option_visible: function (elm) {
            return this.prototype.is_option_visible.call(this, elm);
        },
        lazy_image_load: function () {
            return this.prototype.lazy_image_load.call(this);
        },
    });

    animation.registry.website_snippet_country_phone_code_dropdown =
        CountryPhoneCodeDropdown;
});
