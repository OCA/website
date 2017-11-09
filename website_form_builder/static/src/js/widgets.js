/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_form_builder.widgets', function(require){
    "use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var Model = require('web.Model');
    var options = require('web_editor.snippets.options');
    var widget = require("web_editor.widget");
    var _t = core._t;
    var Dialog = widget.Dialog;

    core.qweb.add_template("/website_form_builder/static/src/xml/widgets.xml");

    return {
        DefaultValueForm: Dialog.extend({
            template: "website_form_builder.DefaultValueForm",

            /**
             * Store needed field information.
             *
             * @param {DOMElement} $field DOM element of the field
             * that wants a new default value.
             */
            init: function (parent, options, field) {
                this.field_html = $(field).html();
                options = $.extend({}, {
                    title: _t("Set field's default value"),
                    size: "small",
                }, options);
                return this._super.call(this, parent, options);
            },

            /**
             * Return the new default value.
             */
            save: function () {
                var inputs = this.$(".o_website_form_input");
                if (inputs.is(":checkbox")) {
                    this.final_data = inputs.filter(":checked")
                    .map(function () {
                        return $(this).val();
                    })
                    .get();
                } else {
                    this.final_data = inputs.val();
                }
                return this._super.apply(this, arguments);
            },
        }),

        HiddenDataForm: Dialog.extend({
            template: "website_form_builder.HiddenDataForm",

            /**
             * Store current data before creating widget
             */
            init: function (parent, options, current_data) {
                this.current_data = "";
                for (var key in current_data) {
                    this.current_data += key + ":" + current_data[key] + "\n";
                }
                options = $.extend({}, {
                    title: _t("Hidden data"),
                }, options);
                return this._super.call(this, parent, options);
            },

            /**
             * Return new hidden data
             */
            save: function () {
                var data = this.$("#data").val().split("\n");
                this.final_data = {};
                for (var line in data) {
                    line = data[line];
                    var combination = line.match(/^([^:]+):(.*)$/);
                    if (!combination) continue;
                    this.final_data[combination[1]] = combination[2];
                }
                return this._super.apply(this, arguments);
            },
        }),

        ParamsForm: Dialog.extend({
            template: "website_form_builder.ParamsForm",

            /**
             * Store models info before creating widget
             */
            init: function (parent, options, models, chosen) {
                this.models = models;
                this.chosen = chosen;
                options = $.extend({}, {
                    title: _t("Form Settings"),
                    size: "small",
                }, options);
                return this._super.call(this, parent, options);
            },

            /**
             * Return model name on save
             */
            save: function () {
                this.final_data = this.$("#model").val();
                return this._super.apply(this, arguments);
            },
        }),

        ModelFieldForm: Dialog.extend({
            template: "website_form_builder.ModelFieldForm",

            /**
             * Store fields info before creating widget
             */
            init: function (parent, options, fields, blacklist) {
                this.fields = fields;
                this.blacklist = blacklist;
                options = $.extend({}, {
                    title: _t("Add Model Field"),
                    size: "small",
                }, options);
                return this._super.call(this, parent, options);
            },

            /**
             * Return field dict on save.
             */
            save: function () {
                var name = this.$("#field").val();
                this.final_data = {
                    name: name,
                    field: this.fields[name],
                };
                return this._super.apply(this, arguments);
            },

            /**
             * Get filtered fields sorted by string.
             *
             * @returns [[string, name], ...]
             */
            sorted_fields: function () {
                var result = [];
                for (var name in this.fields) {
                    var field = this.fields[name];
                    if (
                        name === "id" ||
                        field.readonly ||
                        field.type === "one2many" ||
                        field.type === "reference" ||
                        field.type === "serialized" ||
                        this.blacklist.indexOf(name) !== -1
                    ) {
                        continue;
                    }
                    result.push([field.string, name]);
                }
                result.sort();
                return result;
            },
        })
    };
});
