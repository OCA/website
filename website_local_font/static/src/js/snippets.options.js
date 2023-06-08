/* Copyright 2023 Onestein - Anjeel Haria
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_local_font.editor.snippets.options", function (require) {
    "use strict";

    const website_editor_snippet_options = require("website.editor.snippets.options");
    const FontFamilyPickerUserValueWidget =
        website_editor_snippet_options.FontFamilyPickerUserValueWidget;
    var core = require("web.core");
    var Dialog = require("web.Dialog");
    const weUtils = require("web_editor.utils");
    var _t = core._t;
    var qweb = core.qweb;
    var options = require("web_editor.snippets.options");

    website_editor_snippet_options.FontFamilyPickerUserValueWidget.include({
        xmlDependencies: (
            FontFamilyPickerUserValueWidget.prototype.xmlDependencies || []
        ).concat(["/website_local_font/static/src/xml/website.editor.xml"]),
        events: _.extend({}, FontFamilyPickerUserValueWidget.prototype.events || {}, {
            "click .o_we_add_local_font_btn": "_onAddLocalFontClick",
            "click .o_we_delete_local_font_btn": "_onDeleteLocalFontClick",
        }),
        /**
         * @override
         */
        start: async function () {
            await this._super(...arguments);
            $(this.menuEl).empty();
            const style = window.getComputedStyle(document.documentElement);
            const nbFonts = parseInt(
                weUtils.getCSSVariableValue("number-of-fonts", style)
            );
            const localFontsProperty = weUtils.getCSSVariableValue(
                "local-fonts",
                style
            );
            this.localFonts = localFontsProperty
                ? localFontsProperty.slice(1, -1).split(/\s*,\s*/g)
                : [];
            const fontEls = [];
            const methodName = this.el.dataset.methodName || "customizeWebsiteVariable";
            const variable = this.el.dataset.variable;
            _.times(nbFonts, (fontNb) => {
                const realFontNb = fontNb + 1;
                const fontEl = document.createElement("we-button");
                fontEl.classList.add(`o_we_option_font_${realFontNb}`);
                fontEl.dataset.variable = variable;
                fontEl.dataset[methodName] = weUtils.getCSSVariableValue(
                    `font-number-${realFontNb}`,
                    style
                );
                fontEl.dataset.font = realFontNb;
                fontEls.push(fontEl);
                this.menuEl.appendChild(fontEl);
            });
            if (this.localFonts.length) {
                const localFontsEls = fontEls.splice(-this.localFonts.length);
                localFontsEls.forEach((el, index) => {
                    $(el).append(
                        core.qweb.render("website.delete_local_font_btn", {
                            index: index,
                        })
                    );
                });
            }

            if (this.googleLocalFonts.length) {
                const googleLocalFontsEls = fontEls.splice(
                    -this.googleLocalFonts.length
                );
                googleLocalFontsEls.forEach((el, index) => {
                    $(el).append(
                        core.qweb.render("website.delete_google_font_btn", {
                            index: index,
                            local: true,
                        })
                    );
                });
            }

            if (this.googleFonts.length) {
                const googleFontsEls = fontEls.splice(-this.googleFonts.length);
                googleFontsEls.forEach((el, index) => {
                    $(el).append(
                        core.qweb.render("website.delete_google_font_btn", {
                            index: index,
                        })
                    );
                });
            }

            $(this.menuEl).append(
                $(
                    core.qweb.render("website.add_google_font_btn", {
                        variable: variable,
                    })
                )
            );
            $(this.menuEl).append(
                $(
                    qweb.render("website.add_local_font_btn", {
                        variable: variable,
                    })
                )
            );
        },

        _saveLocalFont: async function () {
            var widgetObj = this.getParent();
            const variable = widgetObj._methodsParams.variable;
            const inputEl = this.el.querySelector(".o_local_input_font");
            const fileEl = this.el.querySelector(".local_font_selection_input");
            if (!inputEl) {
                return;
            }
            const font_name = inputEl.value;
            if (!font_name) {
                inputEl.classList.add("is-invalid");
                return;
            } else if (!fileEl.files) {
                fileEl.classList.add("is-invalid");
                return;
            }
            var allowedExtensions = /(\.otf|\.ttf|\.woff|\.woff2)$/i;
            var file = fileEl.files[0];
            var filename = file.name;
            if (!allowedExtensions.exec(filename)) {
                inputEl.classList.add("is-invalid");
                fileEl.classList.add("is-invalid");
                fileEl.value = "";
                inputEl.value = "";
                return false;
            }
            var extension = filename.substring(
                filename.lastIndexOf(".") + 1,
                filename.length
            );

            const reader = new FileReader();
            const readPromise = new Promise((resolve, reject) => {
                reader.addEventListener("load", () => resolve(reader.result));
                reader.addEventListener("abort", reject);
                reader.addEventListener("error", reject);
                reader.readAsDataURL(fileEl.files[0]);
            });
            const file_data = await readPromise;
            this._rpc({
                model: "ir.attachment",
                method: "add_local_font",
                args: [, font_name, extension, file_data.split(",")[1]],
            }).then((attach_id) => {
                widgetObj.localFonts.push(`'${font_name}': ` + attach_id);
                widgetObj.trigger_up("google_fonts_custo_request", {
                    values: {[variable]: `"${font_name}"`},
                    googleFonts: widgetObj.googleFonts,
                    googleLocalFonts: widgetObj.googleLocalFonts,
                    localFonts: widgetObj.localFonts,
                });
            });
        },

        _onAddLocalFontClick: function () {
            const dialog = new Dialog(this, {
                title: _t("Add a Local Font"),
                $content: $(qweb.render("website.dialog.addLocalFont")),
                buttons: [
                    {
                        text: _t("Save & Reload"),
                        classes: "btn-primary",
                        click: this._saveLocalFont,
                    },
                    {
                        text: _t("Discard"),
                        close: true,
                    },
                ],
            });
            dialog.opened().then(function () {
                dialog.$(".local_font_selection_input").change(function (e) {
                    if (e.target.files) {
                        var filename = e.target.files[0].name;
                        var allowedExtensions = /(\.otf|\.ttf|\.woff|\.woff2)$/i;
                        if (!allowedExtensions.exec(filename)) {
                            e.target.classList.add("is-invalid");
                            e.classList.add("is-invalid");
                            e.target.value = "";
                            e.value = "";
                            return false;
                        }
                        if (filename) {
                            $(".o_local_input_font").val(
                                filename.substring(0, filename.lastIndexOf("."))
                            );
                        }
                    }
                });
            });
            dialog.open();
        },
        /**
         * @private
         * @param {Event} ev
         */
        _onDeleteLocalFontClick: async function (ev) {
            ev.preventDefault();
            const values = {};

            const save = await new Promise((resolve) => {
                Dialog.confirm(
                    this,
                    _t(
                        "Deleting a font requires a reload of the page. This will save all your changes and reload the page, are you sure you want to proceed?"
                    ),
                    {
                        confirm_callback: () => resolve(true),
                        cancel_callback: () => resolve(false),
                    }
                );
            });
            if (!save) {
                return;
            }

            // Remove Local font
            const localFontIndex = parseInt(ev.target.dataset.fontIndex);
            const localFont = this.localFonts[localFontIndex].split(":");
            const localFontName = localFont[0];
            values["delete-local-font-attachment-id"] = localFont[1];
            this.localFonts.splice(localFontIndex, 1);
            // Adapt font variable indexes to the removal
            const style = window.getComputedStyle(document.documentElement);
            _.each(
                FontFamilyPickerUserValueWidget.prototype.fontVariables,
                (variable) => {
                    const value = weUtils.getCSSVariableValue(variable, style);
                    if (value.substring(1, value.length - 1) === localFontName) {
                        // If an element is using the local font being removed, reset
                        // it to the theme default.
                        values[variable] = "null";
                    }
                }
            );

            this.trigger_up("google_fonts_custo_request", {
                values: values,
                googleFonts: this.googleFonts,
                googleLocalFonts: this.googleLocalFonts,
                localFonts: this.localFonts,
            });
        },
    });

    options.Class.include({
        /**
         * @private
         * @param {OdooEvent} ev
         */
        _onGoogleFontsCustoRequest: function (ev) {
            const values = ev.data.values ? _.clone(ev.data.values) : {};
            const localFonts = ev.data.localFonts || ev.target.localFonts;
            if (localFonts !== undefined && localFonts.length) {
                values["local-fonts"] = "(" + localFonts.join(", ") + ")";
            } else {
                values["local-fonts"] = "null";
            }
            ev.data.values = values;
            this._super(...arguments);
        },
    });
});
