/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("website_form_builder.tour", function (require) {
    "use strict";

    // Dependencies here by alphabetic order. Template only for Odoo 9+.
    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    function show_submenus() {
        $(".oe_overlay .dropdown-menu").addClass("show");
    }

    function hide_submenus() {
        $(".oe_overlay .dropdown-menu").removeClass("show");
    }

    var options = {
        url: "/",
        skip_enabled: true,
        test: true,
        wait_for: base.ready(),
    },
    steps = [
        {
            content: "Enter edit mode",
            trigger: "#oe_main_menu_navbar a[data-action=edit]",
        },
        {
            content: "Add a new form",
            run: "drag_and_drop",
            trigger: ".oe_snippet:has(.o_website_form_builder) .oe_snippet_thumbnail",
        },
        {
            content: 'Select "Country"',
            run: "text res.partner.country",
            trigger: ".modal-dialog #model",
        },
        {
            content: "Save",
            trigger: ".modal-dialog .o_save_button",
        },
        {
            content: "Select the form",
            trigger: ".s_website_form[data-model_name='res.partner.country']",
        },
        {
            content: "Customize it",
            trigger: ".oe_overlay .oe_options",
        },
        {
            content: "Add a model field",
            trigger: ".oe_overlay [data-ask_model_field]",
        },
        {
            content: 'Select "Name"',
            run: "text name",
            trigger: ".modal-dialog #field",
        },
        {
            content: "Save",
            trigger: ".modal-dialog .o_save_button",
        },
        {
            content: "Select the new field",
            trigger: "input[name=name]",
        },
        {
            content: "Delete it",
            trigger: ".oe_overlay .oe_snippet_remove",
        },
        {
            content: "Select the form",
            trigger: ".s_website_form[data-model_name='res.partner.country']",
        },
        {
            content: "Customize it",
            trigger: ".oe_overlay .oe_options",
        },
        {
            content: "Add a model field",
            trigger: ".oe_overlay [data-ask_model_field]",
        },
        {
            content: 'Select "Name"',
            run: "text name",
            trigger: ".modal-dialog #field",
        },
        {
            content: "Customize it",
            trigger: ".oe_overlay .oe_options",
        },
        {
            content: "Set a default value",
            trigger: ".oe_overlay [data-ask_default_value]",
        },
        {
            content: _.str.sprintf(
                'Give the default name "%s"',
                "Monkey Island"
            ),
            run: "text Monkey Island",
            trigger: ".modal-dialog [name=name]",
        },
        {
            content: "Save",
            trigger: ".modal-dialog .o_save_button",
        },
        {
            content: "Select the form",
            trigger: ".s_website_form[data-model_name='res.partner.country']",
        },
        {
            content: "Customize it",
            trigger: ".oe_overlay .oe_options",
        },
        {
            content: "Add a custom field",
            run: show_submenus,
            trigger: ".oe_overlay .snippet-option-website_form_builder_form:has(.dropdown-menu)",
        },
        {
            content: "Add a single selection field",
            trigger: '.oe_overlay [data-add_custom_field="selection.radio"]',
        },
        {
            content: "Customize it",
            run: hide_submenus,
            trigger: ".oe_overlay .oe_options",
        },
        {
            content: "Change form action",
            trigger: ".oe_overlay [data-ask_model]",
        },
        {
            content: 'Select "Currency"',
            run: "text res.currency",
            trigger: ".modal-dialog #model",
        },
        {
            content: "Select the custom field",
            trigger: ".form-field-selection.radio",
        },
        {
            content: "Duplicate it",
            trigger: ".oe_overlay .oe_snippet_clone",
        },
        {
            content: "Remove it",
            trigger: ".oe_overlay .oe_snippet_remove",
        },
        {
            content: "Save the page",
            run: "",
            trigger: "#web_editor-top-edit [data-action=save]",
        },
        {
            content: "Change the name",
            run: "text Monkey Island Dollars",
            trigger: "body:not(.editor_enable) .s_website_form[data-model_name='res.currency'] input[name=name]",
        },
        {
            content: "Send the form",
            trigger: ".o_website_form_send",
        },
        {
            content: "Success!",
            trigger: "#o_website_form_result.text-success",
        },
    ];

    tour.register("website_form_builder.tour", options, steps);
});
