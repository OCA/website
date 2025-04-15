/** @odoo-module **/

import {Component, useRef, useState} from "@odoo/owl";
import {renderToElement, renderToFragment} from "@web/core/utils/render";

import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {Dialog} from "@web/core/dialog/dialog";
import {_t} from "@web/core/l10n/translation";
import options from "@web_editor/js/editor/snippets.options";
import {patch} from "@web/core/utils/patch";
import wSnippetOptions from "@website/js/editor/snippets.options";
import weUtils from "@web_editor/js/common/utils";

const ALLOWED_FONT_EXTENSIONS = /(\.otf|\.ttf|\.woff|\.woff2)$/i;
const LOCAL_FONTS_CSS_VAR = "local-fonts";

const FontFamilyPickerUserValueWidget = wSnippetOptions.FontFamilyPickerUserValueWidget;
patch(FontFamilyPickerUserValueWidget.prototype, {
    events: Object.assign({}, FontFamilyPickerUserValueWidget.prototype.events || {}, {
        "click .o_we_add_local_font_btn": "_onAddLocalFontClick",
        "click .o_we_delete_local_font_btn": "_onDeleteLocalFontClick",
    }),

    init() {
        super.init(...arguments);
        this.notification = this.bindService("notification");
        this.dialog = this.bindService("dialog");
        this.orm = this.bindService("orm");
    },

    async start() {
        await super.start(...arguments);

        $(this.menuEl).empty();
        const style = window.getComputedStyle(
            this.$target[0].ownerDocument.documentElement
        );
        const nbFonts =
            parseInt(weUtils.getCSSVariableValue("number-of-fonts", style), 10) || 0;
        const localFontsProperty = weUtils.getCSSVariableValue(
            LOCAL_FONTS_CSS_VAR,
            style
        );
        this.localFonts = localFontsProperty
            ? localFontsProperty.slice(1, -1).split(/\s*,\s*/g)
            : [];

        const fontEls = [];
        const methodName = this.el.dataset.methodName || "customizeWebsiteVariable";
        const variable = this.el.dataset.variable;
        const themeFontsNb =
            nbFonts -
            (this.googleLocalFonts.length +
                this.googleFonts.length +
                this.localFonts.length);
        for (let fontNb = 0; fontNb < nbFonts; fontNb++) {
            const realFontNb = fontNb + 1;
            const fontKey = weUtils.getCSSVariableValue(
                `font-number-${realFontNb}`,
                style
            );
            this.allFonts.push(fontKey);
            let fontName = fontKey.slice(1, -1);
            let fontFamily = fontName;
            const isSystemFonts = fontName === "SYSTEM_FONTS";
            if (isSystemFonts) {
                fontName = _t("System Fonts");
                fontFamily = "var(--o-system-fonts)";
            }
            const fontEl = document.createElement("we-button");
            fontEl.setAttribute("string", fontName);
            fontEl.dataset.variable = variable;
            fontEl.dataset[methodName] = fontKey;
            fontEl.dataset.fontFamily = fontFamily;
            if (realFontNb <= themeFontsNb && !isSystemFonts) {
                // Add the "cloud" icon next to the theme's default fonts
                // because they are served by Google.
                fontEl.appendChild(
                    Object.assign(document.createElement("i"), {
                        role: "button",
                        className: "text-info me-2 fa fa-cloud",
                        title: _t(
                            "This font is hosted and served to your visitors by Google servers"
                        ),
                    })
                );
            }
            fontEls.push(fontEl);
            this.menuEl.appendChild(fontEl);
        }

        if (this.localFonts.length) {
            const localFontsEls = fontEls.splice(-this.localFonts.length);
            localFontsEls.forEach((el, index) => {
                $(el).append(
                    renderToFragment("website.delete_local_font_btn", {
                        index: index,
                        local: "true",
                    })
                );
            });
        }

        if (this.googleLocalFonts.length) {
            const googleLocalFontsEls = fontEls.splice(-this.googleLocalFonts.length);
            googleLocalFontsEls.forEach((el, index) => {
                $(el).append(
                    renderToFragment("website.delete_google_font_btn", {
                        index: index,
                        local: "true",
                    })
                );
            });
        }

        if (this.googleFonts.length) {
            const googleFontsEls = fontEls.splice(-this.googleFonts.length);
            googleFontsEls.forEach((el, index) => {
                $(el).append(
                    renderToFragment("website.delete_google_font_btn", {
                        index: index,
                    })
                );
            });
        }

        $(this.menuEl).append(
            $(
                renderToElement("website.add_google_font_btn", {
                    variable: variable,
                })
            )
        );
        $(this.menuEl).append(
            $(
                renderToElement("website.add_local_font_btn", {
                    variable: this.el.dataset.variable,
                })
            )
        );
    },

    /**
     * Validates a font file
     * @private
     * @param {File} file The file to validate
     * @returns {Object} Validation result {isValid, message}
     */
    _validateFontFile(file) {
        if (!file) {
            return {isValid: false, message: _t("Please select a file")};
        }

        const filename = file.name;
        if (!ALLOWED_FONT_EXTENSIONS.exec(filename)) {
            return {
                isValid: false,
                message: _t(
                    "Invalid file format. Allowed formats: .otf, .ttf, .woff, .woff2"
                ),
            };
        }

        return {isValid: true};
    },

    /**
     * Handler for adding a local font
     * @private
     * @param {Event} event The click event (unused)
     */
    // eslint-disable-next-line no-unused-vars
    _onAddLocalFontClick(event) {
        const variable = this.el.dataset.variable;

        const AddLocalFontDialog = class extends Component {
            static template = "website.dialog.addLocalFont";
            static components = {Dialog};
            static props = {
                close: {type: Function},
                saveFont: {type: Function},
                validateFile: {type: Function},
            };

            setup() {
                this.state = useState({
                    loading: false,
                    fontName: "",
                    fileError: "",
                    nameError: "",
                });
                this.fontFile = useRef("fontFile");
                this.fontName = useRef("fontName");
            }

            /**
             * Handle file input change
             * @param {Event} fileEvent The change event
             */
            onFileChange(fileEvent) {
                this.state.fileError = "";
                fileEvent.target.classList.remove("is-invalid");

                if (!fileEvent.target.files || !fileEvent.target.files.length) {
                    return;
                }

                const file = fileEvent.target.files[0];
                const validation = this.props.validateFile(file);

                if (!validation.isValid) {
                    this.state.fileError = validation.message;
                    fileEvent.target.classList.add("is-invalid");
                    fileEvent.target.value = "";
                    return;
                }

                if (file.name) {
                    this.state.fontName = file.name.substring(
                        0,
                        file.name.lastIndexOf(".")
                    );
                }
            }

            onClickSave() {
                if (this.state.loading) return;

                if (!this.fontName.el.value) {
                    this.state.nameError = _t("Please enter a font name");
                    this.fontName.el.classList.add("is-invalid");
                    return;
                }

                if (!this.fontFile.el.files || !this.fontFile.el.files.length) {
                    this.state.fileError = _t("Please select a file");
                    this.fontFile.el.classList.add("is-invalid");
                    return;
                }

                this.state.loading = true;
                this.props
                    .saveFont(this.fontName.el, this.fontFile.el)
                    .catch((error) => {
                        this.state.loading = false;
                        this.state.fileError =
                            _t("Error uploading font: ") +
                            (error.message || _t("Unknown error"));
                    });

                this.props.close();
            }

            onClickDiscard() {
                this.props.close();
            }
        };

        this.dialog.add(AddLocalFontDialog, {
            title: _t("Add a Local Font"),
            close: () => {
                // Close dialog
            },
            validateFile: this._validateFontFile.bind(this),
            saveFont: async (inputEl, fileEl) => {
                try {
                    const fontName = inputEl.value.trim();
                    const file = fileEl.files[0];

                    if (!fontName || !file) {
                        return Promise.resolve(false);
                    }

                    const validation = this._validateFontFile(file);
                    if (!validation.isValid) {
                        return Promise.resolve(false);
                    }

                    const extension = file.name
                        .substring(file.name.lastIndexOf(".") + 1)
                        .toLowerCase();

                    const fileData = await this._readFileAsBase64(file);
                    if (!fileData) {
                        throw new Error(_t("Failed to read file"));
                    }

                    const attachId = await this.orm.call(
                        "ir.attachment",
                        "add_local_font",
                        [null, fontName, extension, fileData.split(",")[1]],
                        {}
                    );

                    this.localFonts.push(`'${fontName}': ${attachId}`);
                    this._triggerFontUpdate(variable, fontName);
                    return true;
                } catch (error) {
                    this.notification.add(
                        _t("Error adding font: ") +
                            (error.message || _t("Unknown error")),
                        {type: "danger"}
                    );
                    return false;
                }
            },
        });
    },

    /**
     * Reads a file as base64
     * @private
     * @param {File} file The file to read
     * @returns {Promise<String>} Data in base64 format
     */
    _readFileAsBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.onabort = reject;
            reader.readAsDataURL(file);
        });
    },

    /**
     * Triggers event to update fonts
     * @private
     * @param {String} variable CSS variable to update
     * @param {String} fontName Font name
     */
    _triggerFontUpdate(variable, fontName) {
        this.trigger_up("google_fonts_custo_request", {
            values: {[variable]: `"${fontName}"`},
            googleFonts: this.googleFonts,
            googleLocalFonts: this.googleLocalFonts,
            localFonts: this.localFonts,
        });
    },

    /**
     * Handler for deleting a local font
     * @private
     * @param {Event} event The click event
     */
    async _onDeleteLocalFontClick(event) {
        event.preventDefault();

        const confirmed = await this._confirmFontDeletion();
        if (!confirmed) {
            return;
        }

        try {
            const localFontIndex = parseInt(event.target.dataset.fontIndex, 10);
            const fontInfo = this._parseFontInfo(this.localFonts[localFontIndex]);

            const values = {
                "delete-local-font-attachment-id": fontInfo.attachmentId,
            };

            this.localFonts.splice(localFontIndex, 1);

            this._resetFontVariables(values, fontInfo.name);

            this.trigger_up("google_fonts_custo_request", {
                values: values,
                googleFonts: this.googleFonts,
                googleLocalFonts: this.googleLocalFonts,
                localFonts: this.localFonts,
            });
        } catch (error) {
            this.notification.add(
                _t("Error removing font: ") + (error.message || _t("Unknown error")),
                {type: "danger"}
            );
        }
    },

    /**
     * Requests confirmation to delete a font
     * @private
     * @returns {Promise<Boolean>} Confirmation result
     */
    _confirmFontDeletion() {
        return new Promise((resolve) => {
            this.dialog.add(ConfirmationDialog, {
                body: _t(
                    "Deleting a font requires a reload of the page. This will save all your changes and reload the page, are you sure you want to proceed?"
                ),
                confirm: () => resolve(true),
                cancel: () => resolve(false),
            });
        });
    },

    /**
     * Extracts information from a local font
     * @private
     * @param {String} fontString String with font information
     * @returns {Object} Font information {name, attachmentId}
     */
    _parseFontInfo(fontString) {
        const parts = fontString.split(":");
        return {
            name: parts[0].trim().replace(/^'|'$/g, ""),
            attachmentId: parts[1] ? parts[1].trim() : null,
        };
    },

    /**
     * Resets CSS variables that use a specific font
     * @private
     * @param {Object} values Object to store values to update
     * @param {String} fontName Font name to reset
     */
    _resetFontVariables(values, fontName) {
        const style = window.getComputedStyle(document.documentElement);

        FontFamilyPickerUserValueWidget.prototype.fontVariables.forEach((variable) => {
            const value = weUtils.getCSSVariableValue(variable, style);
            if (value && value.substring(1, value.length - 1) === fontName) {
                values[variable] = "null";
            }
        });
    },
});

options.Class.include({
    /**
     * @private
     * @param {OdooEvent} ev
     */
    _onGoogleFontsCustoRequest: function (ev) {
        const values = ev.data.values ? Object.assign({}, ev.data.values) : {};
        const localFonts = ev.data.localFonts || ev.target.localFonts;

        if (localFonts !== undefined && localFonts.length) {
            values[LOCAL_FONTS_CSS_VAR] = "(" + localFonts.join(", ") + ")";
        } else {
            values[LOCAL_FONTS_CSS_VAR] = "null";
        }

        ev.data.values = values;
        this._super(...arguments);
    },
});
