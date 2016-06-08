/* © 2016 Tecnativa, S.L.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */
'use strict';

(function ($) {
    var website = openerp.website;
    var qweb = openerp.qweb;
    var _t = openerp._t;
    website.add_template_file('/website_snippet_country_dropdown/static/src/xml/country_dropdown.xml');

    website.snippet.options.website_snippet_country_dropdown = website.snippet.Option.extend({
        on_prompt: function () {
            var self = this;
            return website.prompt({
                id: "editor_website_snippet_country_dropdown",
                window_title: _t("Country Dropdown Options"),
                input: _t("Field name value"),
                init: function() {
                    // Render tempate
                    var $my_form = $('#editor_website_snippet_country_dropdown');
                    var $group = this.$dialog.find("div.form-group");
                    var $add = $(qweb.render('dropdown_country_helper',{}));
                    $my_form.append($add);
                },
            }).then(function (complete_field_value) {
                var $inputField = self.$target.find("#complete_field")
                if (complete_field_value){
                    $inputField.attr("data-cke-saved-name", complete_field_value);
                } else{
                    // Write default value
                    if ($inputField.attr('name') != 'complete_field'){
                        $inputField.attr("data-cke-saved-name", 'complete_field');
                    };
                };
            });
        },
        drop_and_build_snippet: function() {
            var self = this;
            this._super();
            this.on_prompt().fail(function () {
                self.editor.on_remove();
            });
        },
        start : function () {
            this.$el.find(".js_dropdown_fields").on("click", _.bind(this.on_prompt, this));
            this._super();
        },
    });
})(jQuery);