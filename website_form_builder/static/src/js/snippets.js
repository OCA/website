/* Copyright 2017 Tecnativa - Jairo Llopis
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl). */

odoo.define('website_form_builder.snippets', function (require) {
    "use strict";

    var ajax = require("web.ajax");
    var core = require('web.core');
    var Context = require('web.Context');
    var Domain = require('web.Domain');
    var weContext = require("web_editor.context");
    var options = require('web_editor.snippets.options');
    var widgets = require("website_form_builder.widgets");
    var ServicesMixin = require('web.ServicesMixin');
    var _t = core._t;

    var _fields_asked = {},
        _fields_def = {},
        _models_asked = false,
        _models_def = $.Deferred(),
        _templates_loaded = ajax.loadXML(
            "/website_form_builder/static/src/xml/snippets.xml",
            core.qweb
        );

    /**
     * Lazily ask just once for models.
     *
     * @returns {$.Deferred} Indicates models were loaded.
     */
    function available_models(servicesMixin) {
        if (!_models_asked) {
            servicesMixin._rpc({
                    model: 'ir.model',
                    method: 'search_read',
                    kwargs: {
                        domain: [
                            ["website_form_access", "=", true],
                        ],
                        fields: [
                            "name",
                            "model",
                            "website_form_label",
                        ],
                        order: [{name: 'website_form_label', asc: true}],
                        context: weContext.get()}
                }).done(function (models_list) {
                    _models_def.resolve(_.indexBy(models_list, "model"));
                });
            _models_asked = true;
        }
        return _models_def;
    }

    /**
     * Lazily load just once authorized fields for given model.
     *
     * @param {String} model Model technical name.
     * @returns {$.Deferred} Indicates fields were loaded.
     */
    function authorized_fields(model, servicesMixin) {
        if (!_fields_asked[model]) {
            _fields_def[model] = $.Deferred();
            available_models(servicesMixin).done(function (models) {
                servicesMixin._rpc({
                    model: 'ir.model',
                    method: "get_authorized_fields",
                    args: [models[model].model],
                    kwargs: {
                        context: weContext.get(),
                    }
                }).done($.proxy(
                    _fields_def[model].resolve,
                    _fields_def[model]
                ));
            });
            _fields_asked[model] = true;
        }
        return _fields_def[model];
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

        toggleClass: function (type, value) {
            this._super.apply(this, arguments);
            // Toggle field required attribute to match the container class
            if (type === "reset" || value === "o_required") {
                this.$inputs.attr(
                    "required",
                    this.$target.hasClass("o_required")
                );
            }
            // Ask for a default value if hiding a field without it
            if (
                type === "click" &&
                value === "css_non_editable_mode_hidden" &&
                this.$target.hasClass(value) &&
                // Query to know if there's a default value
                !this.$inputs.filter(
                    // A selectable input is selected...
                    ":checkbox[selected], :radio[selected]," +
                    "select>option[selected]," +
                    // ... or a fillable input is filled
                    "input[value][value!=''],textarea:parent"
                ).length
            ) {
                this.ask_default_value(type);
            }
        },

        /**
         * Prompt the user for a default value for this field.
         *
         * @param {String} type Event type
         * @returns {Dialog} Opened dialog
         */
        ask_default_value: function (type) {
            if (type === "reset") {
                // Nothing to reset here
                return;
            }
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

        cleanForSave: function () {
            var fields = this.present_fields();
            this.ensure_section_send();
            // Sync HTML metadata of custom fields with UI
            this.$("[data-model-field=false]").each(function () {
                var $el = $(this),
                    $label = $el.children(".control-label"),
                    $input = $el.find(".o_website_form_input");
                if (!$label.length) {
                    return;
                }
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
                this._rpc({
                    model: 'ir.model.fields',
                    method: 'formbuilder_whitelist',
                    args: [this.controller_data().model_name, fields],
                    kwargs: {
                        context: weContext.get(),
                    },
                    async: false
                });
            } else {
                // No fields? Destroy snippet before saving
                this.$target.remove();
            }
        },

        /**
         * Ask for a model or remove snippet.
         */
        onBuilt: function () {
            this.ask_model();
            this._super.apply(this, arguments);
            this.ensure_section_send();
        },

        /**
         * Make sure it has a section to send and receive feedback.
         */
        ensure_section_send: function () {
            var send_section = this.$(
                ".form-group:has(.o_website_form_send)" +
                           ":has(#o_website_form_result)"
            );
            if (send_section.is(":visible")) {
                return;
            }
            // Remove possibly garbagey section
            this.$(".o_website_form_fields+.form-group").remove();
            _templates_loaded.done($.proxy(this, "_add_section_send"));
        },

        /**
         * Append a section to send and receive feedback.
         */
        _add_section_send: function () {
            this.$("form").append(core.qweb.render(
                "website_form_builder.section.send",
                {option: this}
            ));
        },

        /**
         * Fetch available models and let user choose one.
         *
         * @param {String} type Event type
         * @returns {$.Deferred} Resolves with the open form
         */
        ask_model: function (type) {
            if (type === "reset") {
                // Nothing to reset here
                return;
            }
            return available_models(this).done($.proxy(this._ask_model, this));
        },

        /**
         * Create and process form widget for asking the model.
         *
         * @param {Object} models ORM records of ir.model objects
         * @returns {Dialog} Open dialog
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
         *
         * @param {String} type Event type
         * @returns {$.Deferred} Resolves with the open dialog
         */
        ask_model_field: function (type) {
            if (type === "reset") {
                // Nothing to reset here
                return;
            }
            return authorized_fields(this.controller_data().model_name, this).done(
                $.proxy(this._ask_model_field, this)
            );
        },

        /**
         * Create and process form widget for choosing the new model field.
         *
         * @param {Array} fields Fields among which user can choose
         * @returns {Dialog} Open dialog
         */
        _ask_model_field: function (fields) {
            var form = new widgets.ModelFieldForm(
                this, {}, fields, this.present_fields()
            );
            form.on("save", this, function (infos) {
                _.map(infos, this.add_model_field, this);
            });
            return form.open();
        },

        /**
         * Inject a new custom field into the form.
         *
         * @param {String} type Event type
         * @param {String} value Custom field type to add
         * @param {jQuery} $li Clicked menu item
         * @returns {jQuery} Added field
         */
        add_custom_field: function (type, value, $li) {
            if (type === "reset") {
                // Nothing to reset here
                return;
            }
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
         * @returns {Array} List of present field names
         */
        present_fields: function () {
            return _.pluck(this.$(":input[name]"), "name");
        },

        /**
         * Change form's target model.
         *
         * @param {String} model Technical model name
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
                authorized_fields(model, this)
                    .done($.proxy(this.reset_model_fields, this));
            }
        },

        /**
         * Empty form's current fields and fill with only required ones.
         *
         * @param {Object} fields ORM ir.model.fields records
         */
        reset_model_fields: function (fields) {
            // Remove old model fields
            this.$(".o_website_form_fields [data-model-field=true]").remove();
            // Add new model required fields by default
            for (var name in fields) {
                if (fields[name].required) {
                    this.add_model_field({
                        name: name,
                        field: fields[name]
                    });
                }
            }
        },

        /**
         * Inject a new field from the model into the form.
         *
         * @param {Object} info {name: field_name, field: field_definition}
         * @returns {$.Deferred} Resolves with the added field jQuery element
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
                    true, _templates_loaded)
                .done($.proxy(this._add_field, this));
        },

        /**
         * Perform insertion of field in form.
         *
         * @param {String} template QWeb field template name to be rendered
         * @param {String} name Field name
         * @param {Object} field Field attributes
         * @param {Array} relational_data Data for x2x fields
         * @param {Boolean} model_field Is it a model field?
         * @returns {jQuery} Appended element
         */
        _add_field: function (template, name, field, relational_data,
            model_field) {
            return this.$(".o_website_form_fields").append(core.qweb.render(
                template, {
                    field: field,
                    model_field: model_field,
                    name: name,
                    relational_data: relational_data,
                    required_att: field.required
                        ? "required"
                        : null,
                    widget: this,
                }
            ));
        },

        /**
         * Selectable options for relational fields.
         *
         * @param {String} field Field name
         * @returns {$.Deferred} ORM results
         */
        relational_options: function (field) {
            var domain = [],
                context = weContext.get();
            // Domain might contain un-evaluable literals
            try {
                domain = new Domain(field.domain || [], weContext.get()).toArray();
            } catch (error) {
                // eslint-disable-next-line no-console
                console.warn("Cannot evaluate field domain, ignoring.");
            }
            // Context too
            try {
                context = new Context(
                    weContext.get(),
                    field.context
                ).eval();
            } catch (error) {
                // eslint-disable-next-line no-console
                console.warn("Cannot evaluate field context, using user's.");
            }
            // Get results
            return this._rpc({
                model: field.relation,
                method: 'search_read',
                kwargs: {
                    domain: domain,
                    fields: ["display_name"],
                    order: [{name: "display_name", asc: true}],
                    context: context,
                }
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
    };
});
