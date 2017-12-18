/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_form_builder.snippets', function(require){
    "use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var Model = require('web.Model');
    var options = require('web_editor.snippets.options');
    var _t = core._t;
    var widgets = require("website_form_builder.widgets");
    var data = require("web.data");

    core.qweb.add_template(
        "/website_form_builder/static/src/xml/snippets.xml"
    );

    var _fields_asked = {},
        _fields_def = {},
        _models_asked = false,
        _models_def = $.Deferred();

    /**
     * Lazily load just once authorized fields for given model.
     */
    function authorized_fields (model) {
        if (!_fields_asked[model]) {
            _fields_def[model] = $.Deferred();
            available_models().done(function (models) {
                new Model("ir.model").call(
                    "get_authorized_fields",
                    [models[model].id],
                    {context: base.get_context()}
                ).done($.proxy(
                    _fields_def[model].resolve,
                    _fields_def[model]
                ));
            });
            _fields_asked[model] = true;
        }
        return _fields_def[model];
    }

    /**
     * Lazily ask just once for models.
     */
    function available_models () {
        if (!_models_asked) {
            new Model("ir.model").call("search_read", {
                domain: [
                    ["website_form_access", "=", true],
                ],
                fields: [
                    "name",
                    "model",
                    "website_form_label",
                ],
                order: "website_form_label",
                context: base.get_context(),
            }).done(function (models_list) {
                _models_def.resolve(_.indexBy(models_list, "model"));
            });
            _models_asked = true;
        }
        return _models_def;
    }

    var Field = options.Class.extend({
        /**
         * Disables the action buttons forbidden for current field.
         *
         * It loads overlay selectors to disable from the `data-disable`
         * attribute set when using the option.
         */
        start: function () {
            this._super.apply(this, arguments);
            this.$inputs = this.$(".o_website_form_input");
            if (this.data.disable) {
                this.disable_buttons(this.data.disable);
            }
            // Cross-browser editable labels
            // HACK https://bugzilla.mozilla.org/show_bug.cgi?id=853519
            this.$("label").prop("contentEditable", false)
                .children("span").prop("contentEditable", true);
        },

        toggle_class: function (type, value, $li) {
            this._super.apply(this, arguments);
            // Toggle field required attribute to match the container class
            if (type === "reset" || value === "o_required") {
                this.$inputs.attr(
                    "required",
                    this.$target.hasClass("o_required")
                );
            }
        },

        /**
         * Prompt the user for a default value for this field.
         */
        ask_default_value: function (type, value, $li) {
            if (type === "reset") return; // Nothing to reset here
            var form = new widgets.DefaultValueForm(this, {}, this.$target);
            form.on("save", this, this.set_default_value);
            return form.open();
        },

        /**
         * Set the new default value for the field.
         *
         * @param {Array|String} default_value It will be a `String` indicating
         * the new default value, unless `this.$input` is a checkbox, in which
         * case it will be an `Array` that contains the value of the check
         * boxes that must be enabled by default.
         */
        set_default_value: function (default_value) {
            var $inputs = this.$inputs;
            if ($inputs.is(":checkbox,:radio")) {
                // Set as checked chosen boxes
                $inputs.each(function () {
                    $(this).attr(
                        "checked",
                        $.inArray($(this).val(), default_value) !== -1
                    );

                });
            } else if ($inputs.is("select")) {
                // Set as selected chosen option
                $inputs.find("option").each(function () {
                    $(this).attr(
                        "selected",
                        $(this).attr("value") === default_value
                    );
                });
            } else {
                // Simply put the new default value in the element
                $inputs.attr("value", default_value || "");
            }
        },

        /**
         * Disables an action button.
         *
         * @param {String} selector It should be `.oe_snippet_move`,
         * `.oe_snippet_clone`, or `.oe_snippet_remove`
         * (or comma-separated combinations of them).
         */
        disable_buttons: function (selector) {
            var button = this.$overlay.find(selector);
            button.addClass("disabled");
        },
    });

    var Form = options.Class.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.$form = this.$("form.s_website_form");
        },

        clean_for_save: function () {
            var fields = this.present_fields();
            // Sync HTML metadata of custom fields with UI
            this.$("[data-model-field=false]").each(function () {
                var $el = $(this),
                    $label = $el.children(".control-label"),
                    $input = $el.find(".o_website_form_input");
                if (!$label.length) return;
                $input.attr("name", _.str.clean($label.text()));
                $input.filter(":checkbox, :radio").each(function () {
                    var $box = $(this);
                    $box.attr(
                        "value",
                        _.str.clean($box.closest("label").text())
                    );
                });
            });
            // Remove any content in the form result
            this.$("#o_website_form_result").removeAttr("class").empty();
            // Do not save disabled send button
            this.$(".o_website_form_send").removeClass("disabled");
            // Do not save fields error status
            this.$(".has-error").removeClass("has-error");
            if (fields.length) {
                // Whitelist model fields found in current form
                new Model("ir.model.fields").call(
                    "formbuilder_whitelist",
                    [this.controller_data().model_name, fields],
                    {context: base.get_context()},
                    {async: false} // Do not save until done
                );
            } else {
                // No fields? Destroy snippet before saving
                this.$target.remove();
            }
        },

        /**
         * Ask for a model or remove snippet.
         */
        drop_and_build_snippet: function () {
            this.ask_model();
            return this._super.apply(this, arguments);
        },

        /**
         * Let user set hidden data for the form.
         */
        ask_hidden_data: function (type) {
            if (type === "reset") return; // Nothing to reset here
            var form = new widgets.HiddenDataForm(
                this, {}, this.controller_data().hidden_data
            );
            form.on("save", this, this.set_hidden_data);
            return form.open();
        },

        /**
         * Set form's hidden data.
         */
        set_hidden_data: function (new_data) {
            var old_data = this.controller_data().hidden_data;
            for (var key in old_data) {
                if (!(key in new_data)) {
                    this.$form.removeAttr("data-form_field_" + key);
                }
            }
            for (var key in new_data) {
                this.$form.attr("data-form_field_" + key, new_data[key]);
            }
        },

        /**
         * Fetch available models and let user choose one.
         */
        ask_model: function (type) {
            if (type === "reset") return; // Nothing to reset here
            return available_models().done($.proxy(this._ask_model, this));
        },

        /**
         * Create and process form widget for asking the model.
         */
        _ask_model: function (models) {
            var form = new widgets.ParamsForm(
                this, {}, models, this.controller_data().model_name
            );
            form.on("save cancel", this, this.set_model);
            return form.open();
        },

        /**
         * Fetch available fields from model and let user choose one.
         */
        ask_model_field: function (type) {
            if (type === "reset") return; // Nothing to reset here
            return authorized_fields(this.controller_data().model_name).done(
                $.proxy(this._ask_model_field, this)
            );
        },

        /**
         * Create and process form widget for choosing the new model field.
         */
        _ask_model_field: function (fields) {
            var form = new widgets.ModelFieldForm(
                this, {}, fields, this.present_fields()
            );
            form.on("save", this, this.add_model_field);
            return form.open();
        },

        /**
         * Inject a new custom field into the form.
         */
        add_custom_field: function (type, value, $li) {
            if (type === "reset") return; // Nothing to reset here
            var name = _.str.sprintf(
                    _t("Custom %s field"),
                    _.str.clean($li.text())
                ),
                option = _t("Option %d"),
                field = {
                    required: false,
                    help: _.str.sprintf(
                        _t("%s help block"),
                        name
                    ),
                    string: name,
                    // Default values for selection fields
                    selection: _.map(_.range(1, 5), function (num) {
                        return [null, _.str.sprintf(option, num)];
                    }),
                    type: value,
                };
            return this._add_field(
                _.str.sprintf("website_form_builder.field.%s", value),
                name,
                field,
                // Default values for many2* fields
                _.map(_.range(1, 5), function (num) {
                    return {
                        id: null,
                        display_name: _.str.sprintf(option, num),
                    };
                }),
                false
            );
        },

        /**
         * Get current form's controller data.
         *
         * @returns {Object} Form-attached data that is used by the
         * `website_form.animation` JS module. Check its source code to know
         * what they do.
         */
        controller_data: function () {
            var hidden_data = {},
                attributes = Array.prototype.slice.call(
                    this.$form[0].attributes);
            for (var attr in attributes) {
                attr = attributes[attr];
                if (_.str.startsWith(attr.name, 'data-form_field_')) {
                    hidden_data[attr.name.substr(16)] = attr.value;
                }
            }
            return {
                force_action: this.$form.attr("data-force_action"),
                hidden_data: hidden_data,
                model_name: this.$form.attr("data-model_name"),
                success_page: this.$form.attr("data-success_page"),
            };
        },

        /**
         * List present fields.
         *
         * @returns Array
         */
        present_fields: function () {
            return _.pluck(this.$(":input[name]"), "name");
        },

        /**
         * Change form's target model.
         */
        set_model: function (model) {
            var previous_model = this.controller_data().model_name;
            if (!model && !previous_model) {
                // No model? Destroy snippet
                this.$target.remove();
                return;
            }
            this.$form.attr("data-model_name", model);
            // Model changed? Load new fields and reset snippet
            if (previous_model !== model) {
                authorized_fields(model)
                    .done($.proxy(this.reset_model_fields, this));
            }
        },

        /**
         * Empty form's current fields and fill with only required ones.
         */
        reset_model_fields: function (fields) {
            // Remove old model fields
            this.$(".o_website_form_fields [data-model-field=true]").remove();
            // Add new model required fields by default
            for (name in fields) {
                if (fields[name].required) {
                    this.add_model_field({name: name, field: fields[name]});
                }
            }
        },

        /**
         * Inject a new field from the model into the form.
         *
         * @param {name: field_name, field: field_definition} info
         */
        add_model_field: function (info) {
            var relational_data = [],
                template = _.str.sprintf(
                    "website_form_builder.field.%s",
                    info.field.type
                );
            if (info.field.type.indexOf("many") !== -1) {
                relational_data = this.relational_options(info.field);
            }
            return $.when(template, info.name, info.field, relational_data,
                          true)
                .done($.proxy(this._add_field, this));
        },

        /**
         * Perform insertion of field in form.
         *
         * @param {String} template QWeb field template name to be rendered
         * @param {String} name Field name
         * @param {Object} field Field attributes
         * @param {Array[Object]} relational_data Data for x2x fields
         * @param {Boolean} model_field Is it a model field?
         */
        _add_field: function (template, name, field, relational_data,
                              model_field) {
            return this.$(".o_website_form_fields").append(core.qweb.render(
                template,
                {
                    field: field,
                    model_field: model_field,
                    name: name,
                    relational_data: relational_data,
                    required_att: field.required ? "required" : null,
                    widget: this,
                }
            ));
        },

        /**
         * Selectable options for relational fields.
         */
        relational_options: function (field) {
            var domain = [], context = base.get_context();
            // Domain might contain un-evaluable literals
            try {
                domain = new data.CompoundDomain(field.domain || []).eval();
            } catch (error) {
                console.warn("Cannot evaluate field domain, ignoring.");
            }
            // Context too
            try {
                context = new data.CompoundContext(
                    base.get_context(),
                    field.context
                ).eval();
            } catch (error) {
                console.warn("Cannot evaluate field context, using user's.");
            }
            // Get results
            return new Model(field.relation).call("search_read", {
                domain: domain,
                fields: ["display_name"],
                order: "display_name",
                context: context,
            });
        },
    });

    // Add options to registry
    options.registry.website_form_builder_field = Field;
    options.registry.website_form_builder_form = Form;

    return {
        authorized_fields: authorized_fields,
        available_models: available_models,
        Field: Field,
        Form: Form,
    }
});
