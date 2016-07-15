/* © 2016 Tecnativa, S.L.
 * © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */
odoo.define("website_snippet_country_dropdown.editor", function (require) {
    "use strict";

    var core = require("web.core"),
        options = require("web_editor.snippets.options"),
        website = require("website.website"),
        $ = require("$");

    // Load once the template
    core.qweb.add_template(
        '/website_snippet_country_dropdown/static/src/xml/country_dropdown.xml'
    );

    return options.registry.country_dropdown = options.Class.extend({
        tpl_name: 'website_snippet_country_dropdown.helper',
        ask_field_name: function (type, $li) {
            if (type != "click") {
                return $.Deferred().reject();
            }
            return website.prompt({
                id: "editor_website_snippet_country_dropdown",
                window_title: core._t("Country Dropdown Options"),
                input: core._t("Complete field name"),
                init: $.proxy(this.prompt_render, this),
            }).done($.proxy(this.change_name, this));
        },
        prompt_render: function (field, dialog) {
            dialog.find(".modal-body")
            .append(core.qweb.render(this.tpl_name));
            return this.$target.find("#complete_field").attr("name");
        },
        change_name: function (complete_field_value, dialog) {
            complete_field_value = complete_field_value || 'complete_field';
            this.$target.find("#complete_field").attr({
                "name": complete_field_value,
                "data-cke-saved-name": complete_field_value,
            });
        },
        drop_and_build_snippet: function () {
            // Set a name to the snippet or delete it
            var remove_button = this.$overlay.find(".oe_snippet_remove");
            this.ask_field_name("click").fail($.proxy(
                remove_button.click, remove_button
            ));

            return this._super();
        },
    });
});
