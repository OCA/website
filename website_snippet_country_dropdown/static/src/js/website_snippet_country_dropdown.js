/* Copyright 2016 Tecnativa, S.L.
 * Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * Copyright 2019 Alexandre Díaz <alexandre.diaz@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_country_dropdown.dropdown", function (require) {
    "use strict";
    var animation = require('website.content.snippets.animation');

    var CountryDropdown = animation.Class.extend({
        selector: ".js_country_dropdown",
        start: function () {
            this._super.apply(this, arguments);
            this.$flag_selector = this.$target.find('.js_select_country_code');
            this.$img_code = this.$target.find('.js_img_country_code');
            this.$btn_country_code = this.$target.find('.js_btn_country_code');
            this.$dropdown_list = this.$target.find('#dropdown-countries');
            this.$country_code_field = this.$target.find(
                '.js_country_code_field');
            this.$no_country_field = this.$target.find('.js_no_country_field');
            this.$complete_field_post = this.$target.find(
                '.js_complete_field_post');
            this.$flag_selector.on('click', $.proxy(this.set_value, this));
            this.$no_country_field.on(
                'change',
                $.proxy(this.on_change_no_country_field, this)
            );
            this.$dropdown_list.on(
                'scroll',
                _.debounce(this.lazy_image_load.bind(this), 35)
            );
            this.$target.on(
                'shown.bs.dropdown',
                this.lazy_image_load.bind(this));
        },
        set_value: function (event) {
            this.country_code = event.currentTarget.id;
            this.$flag_selector.val(event.currentTarget.id);
            this.$img_code.attr(
                "src",
                "/website/image/res.country/" +
                event.currentTarget.dataset.country_id +
                "/image/30x20"
            );
            this.$btn_country_code.attr("data-country_code", event.currentTarget.dataset.country_code);
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

        is_option_visible: function (elm) {
            var ddViewTop = this.$dropdown_list.offset().top;
            var ddViewBottom = ddViewTop + this.$dropdown_list.height();

            var elemTop = elm.offset().top;
            var elemBottom = elemTop + elm.height();

            return elemTop <= ddViewBottom && elemBottom >= ddViewTop;
        },
        lazy_image_load: function () {
            var self = this;
            this.$dropdown_list.children('a').each(function () {
                var $elm = $(this);
                var $img = $elm.children('img');
                if (!$img.attr('src') && self.is_option_visible($elm)) {
                    $elm.children('img').attr(
                        'src',
                        "/website/image/res.country/" +
                        $elm.data('country_id') +
                        "/image/30x20");
                }
            });
        },
    });

    animation.registry.website_snippet_country_dropdown = CountryDropdown;
});
