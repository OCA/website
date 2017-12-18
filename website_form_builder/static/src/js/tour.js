/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define("website_form_builder.tour", function (require) {
    "use strict";

    // Dependencies here by alphabetic order. Template only for Odoo 9+.
    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    function show_submenus() {
        $(".oe_overlay_options:visible .dropdown-menu").addClass("show");
    }

    function hide_submenus() {
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
            trigger: ".oe_snippet:has(.o_website_form_builder) .oe_snippet_thumbnail",
        },
        {
            run: "text res.country",
            trigger: ".modal-dialog #model",
        },
        {
            trigger: ".modal-dialog .o_save_button",
        },
        {
            trigger: ".s_website_form[data-model_name='res.country']",
        },
        {
            trigger: ".oe_overlay_options:visible .btn:contains('Customize')",
        },
        {
            trigger: ".oe_overlay_options:visible [data-ask_model_field]>a",
        },
        {
            run: "text name",
            trigger: ".modal-dialog #field",
        },
        {
            trigger: ".modal-dialog .o_save_button",
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
            trigger: ".oe_overlay_options:visible .btn:contains('Customize')",
        },
        {
            trigger: ".oe_overlay_options:visible [data-ask_model_field]>a",
        },
        {
            run: "text name",
            trigger: ".modal-dialog #field",
        },
        {
            trigger: ".modal-dialog .o_save_button",
        },
        {
            trigger: ".form-field label[for=name]",
        },
        {
            trigger: ".oe_overlay_options:visible .btn:contains('Customize')",
        },
        {
            trigger: ".oe_overlay_options:visible [data-ask_default_value]>a",
        },
        {
            run: "text Monkey Island",
            trigger: ".modal-dialog [name=name]",
        },
        {
            trigger: ".modal-dialog .o_save_button",
        },
        {
            trigger: ".s_website_form[data-model_name='res.country']",
        },
        {
            trigger: ".oe_overlay_options:visible .btn:contains('Customize')",
        },
        {
            run: show_submenus,
            trigger: ".oe_overlay_options:visible .snippet-option-website_form_builder_form:has(.dropdown-menu)",
        },
        {
            trigger: '.oe_overlay_options:visible [data-add_custom_field="selection-radio"]>a',
        },
        {
            run: hide_submenus,
            trigger: ".form-field-selection-radio",
        },
        {
            trigger: ".oe_overlay_options:visible .btn:contains('Customize')",
        },
        {
            trigger: ".oe_overlay_options:visible [data-ask_model]>a",
        },
        {
            run: "text res.currency",
            trigger: ".modal-dialog #model",
        },
        {
            trigger: ".modal-dialog .o_save_button",
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
            run: "text Monkey Island Dollars",
            trigger: "body:not(.editor_enable) .s_website_form[data-model_name='res.currency'] input[name=name]",
        },
        {
            trigger: ".o_website_form_send",
        },
        {
            trigger: "#o_website_form_result.text-danger",
        },
        {
            run: "text 🐵",
            trigger: "body:not(.editor_enable) .s_website_form[data-model_name='res.currency'] .has-error input[name=symbol]",
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
