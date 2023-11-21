/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import {renderToElement} from "@web/core/utils/render";

options.registry.WebsiteFormEditor.include({
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
            const labelWidth = this.$target[0].querySelector(".s_website_form_label")
                .style.width;
            template.content.append(
                renderToElement("website_form_require_legal.s_website_form_legal", {
                    labelWidth: labelWidth,
                    termsURL: "terms",
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
