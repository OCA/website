/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

 odoo.define('website_form_builder.widgets', function (require) {
     "use strict";

    var ajax = require("web.ajax");
    var core = require('web.core');
    var widget = require("web_editor.widget");
    var _t = core._t;
    var Dialog = widget.Dialog;

    var result = $.Deferred(),
        _templates_loaded = ajax.loadXML(
            "/website_form_builder/static/src/xml/widgets.xml",
            core.qweb
        );

    var DefaultValueForm = Dialog.extend({
        template: "website_form_builder.DefaultValueForm",

        /**
         * Store needed field information.
         *
         * @param {Object} parent Widget where this dialog is attached
         * @param {Object} options Dialog creation options
         * @param {DOMElement} field Field asking for a new default value
         * @returns {Dialog} New Dialog object
         */
        init: function (parent, options, field) {
            this.field_html = $(field).html();
            var _options = $.extend({}, {
                title: _t("Set field's default value"),
                size: "small",
            }, options);
            return this._super(parent, _options);
        },

        /**
         * Save the new default value.
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
            this._super.apply(this, arguments);
        },
    });

    var ParamsForm = Dialog.extend({
        template: "website_form_builder.ParamsForm",

        /**
         * Store models info before creating widget
         *
         * @param {Object} parent Widget where this dialog is attached
         * @param {Object} options Dialog creation options
         * @param {Array} models Available models to choose among
         * @param {String} chosen Prechosen model
         * @returns {Dialog} New Dialog object
         */
        init: function (parent, options, models, chosen) {
            this.models = models;
            this.chosen = chosen;
            var _options = $.extend({}, {
                title: _t("Form Settings"),
                size: "small",
            }, options);
            return this._super(parent, _options);
        },

        /**
         * Save new model
         */
        save: function () {
            this.final_data = this.$("#model").val();
            this._super.apply(this, arguments);
        },
    });

    var ModelFieldForm = Dialog.extend({
        template: "website_form_builder.ModelFieldForm",

        /**
         * Store fields info before creating widget
         *
         * @param {Object} parent Widget where this dialog is attached
         * @param {Object} options Dialog creation options
         * @param {Array} fields Model's fields
         * @param {Array} blacklist Fields that cannot be chosen
         * @returns {Dialog} New Dialog object
         */
        init: function (parent, options, fields, blacklist) {
            this.fields = fields;
            this.blacklist = blacklist;
            var _options = $.extend({}, {
                title: _t("Add Model Fields"),
                size: "small",
            }, options);
            return this._super(parent, _options);
        },

        /**
         * Save field dict
         */
        save: function () {
            var names = this.$("#field").val();
            this.final_data = [];
            for (var n in names) {
                var name = names[n];
                this.final_data.push({
                    name: name,
                    field: this.fields[name],
                });
            }
            this._super.apply(this, arguments);
        },

        /**
         * Get filtered fields sorted by string.
         *
         * @returns {Array} [[string, name], ...]
         */
        sorted_fields: function () {
            var _result = [];
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
                _result.push([field.string, name]);
            }
            _result.sort();
            return _result;
        },
    });

    // Resolve when finished loading templates
    _templates_loaded.done(function () {
        result.resolve({
            DefaultValueForm: DefaultValueForm,
            ParamsForm: ParamsForm,
            ModelFieldForm: ModelFieldForm,
        });
    });

    return result;
});
