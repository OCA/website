/* Copyright 2017 Tecnativa - Jairo Llopis
   Copyright 2019 Tecnativa - Alexandre Díaz
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("website_form_builder.tour", function (require) {
    "use strict";

    // Dependencies here by alphabetic order. Template only for Odoo 9+.
    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    function show_submenus () {
        $(".oe_overlay_options:visible .dropdown-menu").addClass("show");
    }

    function hide_submenus () {
        $(".oe_overlay_options .dropdown-menu").removeClass("show");
    }

    var options = {
            url: "/",
            skip_enabled: true,
            test: true,
            wait_for: base.ready(),
        },
        steps = [
            {
                trigger: "#oe_main_menu_navbar a[data-action=edit]",
            },
            {
                run: "drag_and_drop",
                trigger:
                    ".oe_snippet:has(.o_website_form_builder) " +
                    ".oe_snippet_thumbnail",
            },
            {
                run: "text res.country",
                trigger: ".modal-dialog #model",
            },
            {
                trigger: ".modal-dialog .btn-primary:contains('Save')",
            },
            {
                trigger: ".s_website_form[data-model_name='res.country']",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger: ".oe_overlay_options:visible [data-ask_model_field]",
            },
            {
                run: "text name",
                trigger: ".modal-dialog #field",
            },
            {
                trigger: ".modal-dialog .btn-primary:contains('Save')",
            },
            {
                trigger: "input[name=name]",
            },
            {
                trigger: ".oe_overlay_options:visible .oe_snippet_remove",
            },
            {
                trigger: ".s_website_form[data-model_name='res.country']",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger: ".oe_overlay_options:visible [data-ask_model_field]",
            },
            {
                run: "text name",
                trigger: ".modal-dialog #field",
            },
            {
                trigger: ".modal-dialog .btn-primary:contains('Save')",
            },
            {
                trigger: ".form-field label[for=name]",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger:
                    ".oe_overlay_options:visible [data-ask_default_value]",
            },
            {
                run: "text Monkey Island",
                trigger: ".modal-dialog [name=name]",
            },
            {
                trigger: ".modal-dialog .btn-primary:contains('Save')",
            },
            {
                trigger: ".s_website_form[data-model_name='res.country']",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                run: show_submenus,
                trigger:
                    ".oe_overlay_options:visible " +
                    ".snippet-option-website_form_builder_form" +
                    ":has(.dropdown-menu)",
            },
            {
                trigger:
                    '.oe_overlay_options:visible ' +
                    '[data-add_custom_field="selection-radio"]',
            },
            {
                trigger: ".form-field-selection-radio",
            },
            // Add a custom text input
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger:
                    '.oe_overlay_options:visible a[data-add_custom_field="char"]',
            },
            // Make it required
            {
                trigger: ".form-field-char[data-optional='true']",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger: ".oe_overlay_options:visible a[data-toggle-class='o_required']",
            },
            // Make it hidden
            {
                run: hide_submenus,
                trigger: ".form-field-char.o_required[data-optional='true'] input[required]",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger: ".oe_overlay_options:visible a:contains('Hide field')",
            },
            // Hiding a required field asks user for a default value; fill it
            {
                run: "text my default",
                trigger: ".modal-dialog .o_website_form_input",
            },
            {
                trigger: ".modal-dialog .btn:contains('Save')",
            },
            // Remove the custom text field
            {
                trigger: ".form-field-char.o_required.css_non_editable_mode_hidden[data-optional='true'] input[required][value='my default']",
            },
            {
                trigger:
                    ".oe_overlay_options:visible .btn:contains('Customize')",
            },
            {
                trigger: ".oe_overlay_options:visible [data-ask_model]",
            },
            {
                run: "text res.currency",
                trigger: ".modal-dialog #model",
            },
            {
                trigger: ".modal-dialog .btn-primary:contains('Save')",
            },
            {
                trigger: ".form-field-selection-radio",
            },
            {
                trigger: ".oe_overlay_options:visible .oe_snippet_clone",
            },
            {
                trigger: ".oe_overlay_options:visible .oe_snippet_remove",
            },
            {
                trigger: "#web_editor-top-edit [data-action=save]",
            },
            {
                run: "text MID",
                trigger:
                    "body:not(.editor_enable) " +
                    ".s_website_form[data-model_name='res.currency'] " +
                    "input[name=name]",
            },
            {
                trigger: ".o_website_form_send",
            },
            {
                trigger: "#o_website_form_result.text-danger",
            },
            {
                run: "text 🐵",
                trigger:
                    "body:not(.editor_enable) " +
                    ".s_website_form[data-model_name='res.currency'] " +
                    ".o_has_error input[name=symbol]",
            },
            {
                trigger: ".o_website_form_send",
            },
            {
                trigger: "#o_website_form_result.text-success",
            },
        ];

    tour.register("website_form_builder.tour", options, steps);
});
