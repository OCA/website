/* © 2016 Tecnativa, S.L.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */
'use strict';
(function ($) {
    var website = openerp.website,
        qweb = openerp.qweb;

    website.snippet.animationRegistry.countryDropdown = website.snippet.Animation.extend({
        selector: ".js_country_dropdown",
        start: function () {
            this.$flag_selector = this.$('.js_select_country_code');
            this.$img_code = this.$('.js_img_country_code');
            this.$btn_country_code = this.$('.js_btn_country_code');
            this.$country_code = this.$('.js_country_code');
            this.$country_code_field = this.$('.js_country_code_field');
            this.$no_country_field = this.$('.js_no_country_field');
            this.$complete_field_post = this.$('.js_complete_field_post');
            var self = this;
            this.$flag_selector.on('click', function(event) {
                return self.set_value(event);
            });
            this.$no_country_field.change(function(event){
                return self.join_value(self.$country_code_field.val(), this.value);
            });
        },
        set_value: function(event){
            this.country_code = event.currentTarget.id;
            this.$flag_selector.val(event.currentTarget.id);
            this.$img_code.attr("src", "/website/image/res.country/"+ event.currentTarget.dataset.country_id +"/image/30x20");
            this.$btn_country_code.val(event.currentTarget.dataset.country_id);
            this.$country_code_field.val(event.currentTarget.id);
            this.$country_code.children().text(String(event.currentTarget.id));
            this.join_value(event.currentTarget.id, this.$no_country_field.val());
        },
        join_value: function(country_code, value){
            this.$complete_field_post.val(country_code.concat(value));
        }
    });
})(jQuery);
