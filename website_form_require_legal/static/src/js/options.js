odoo.define("website_form_require_legal.form_editor", function (require) {
    "use strict";

    const core = require("web.core");
    const options = require("web_editor.snippets.options");
    require("website.editor.snippets.options");

    const qweb = core.qweb;
    const WebsiteFormEditor = options.registry.WebsiteFormEditor;

    WebsiteFormEditor.include({
        xmlDependencies: (WebsiteFormEditor.prototype.xmlDependencies || []).concat([
            "/website_form_require_legal/static/src/xml/website_form_editor.xml",
        ]),
        /**
         * @override
         */
        start: function () {
            const proms = [this._super(...arguments)];
            this.$target.find(".s_website_form_legal").attr("contentEditable", true);
            return Promise.all(proms);
        },
        /**
         * Toggle the legal terms checkbox
         */
        toggleLegalTerms: function () {
            const legalTermsEl = this.$target[0].querySelector(".s_website_form_legal");
            if (legalTermsEl) {
                legalTermsEl.remove();
            } else {
                const template = document.createElement("template");
                const labelWidth = this.$target[0].querySelector(
                    ".s_website_form_label"
                ).style.width;
                $(template).html(
                    qweb.render("website_form_require_legal.s_website_form_legal", {
                        labelWidth: labelWidth,
                        termsURL: "/terms",
                    })
                );
                const legal = template.content.firstElementChild;
                legal.setAttribute("contentEditable", true);
                if (this.$target.find(".s_website_form_recaptcha").length) {
                    this.$target.find(".s_website_form_recaptcha")[0].before(legal);
                } else {
                    this.$target.find(".s_website_form_submit").before(legal);
                }
            }
        },
        /**
         * @override
         */
        _computeWidgetState: function (methodName) {
            if (methodName === "toggleLegalTerms") {
                return !this.$target[0].querySelector(".s_website_form_legal") || "";
            }
            return this._super(...arguments);
        },
    });
});
