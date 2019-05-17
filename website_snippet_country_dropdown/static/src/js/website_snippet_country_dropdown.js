/* © 2016 Tecnativa, S.L.
 * © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_country_dropdown.dropdown", function (require) {
    "use strict";
    var animation = require("web_editor.snippets.animation");

    animation.registry.countryDropdown = animation.Class.extend({
        selector: ".js_country_dropdown",
        start: function () {
            this.$flag_selector = this.$('.js_select_country_code');
            this.$img_code = this.$('.js_img_country_code');
            this.$btn_country_code = this.$('.js_btn_country_code');
            this.$country_code = this.$('.js_country_code');
            this.$country_code_field = this.$('.js_country_code_field');
            this.$no_country_field = this.$('.js_no_country_field');
            this.$complete_field_post = this.$('.js_complete_field_post');
            this.$flag_selector.on('click', $.proxy(this.set_value, this));
            this.$no_country_field.on(
                'change',
                $.proxy(this.on_change_no_country_field, this)
            );
        },
        set_value: function (event) {
            this.country_code = event.currentTarget.id;
            this.$flag_selector.val(event.currentTarget.id);
            this.$img_code.attr(
                "src",
                "/website/image/res.country/" +
                event.currentTarget.dataset.country_id+
                "/image/30x20"
            );
            this.$btn_country_code.val(event.currentTarget.dataset.country_id);
            this.$country_code_field.val(event.currentTarget.id);
            this.$country_code.children().text(String(event.currentTarget.id));
            this.join_value(
                event.currentTarget.id,
                this.$no_country_field.val()
            );
        },
        join_value: function (country_code, value) {
            this.$complete_field_post.val(country_code.concat(value));
        },
        on_change_no_country_field: function () {
            return this.join_value(
                this.$country_code_field.val(),
                this.$no_country_field.val()
            );
        },
    });

    return animation.registry.countryDropdown;
});
