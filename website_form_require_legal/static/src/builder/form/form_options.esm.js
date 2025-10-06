import {BuilderAction} from "@html_builder/core/builder_action";
import {Plugin} from "@html_editor/plugin";
import {patch} from "@web/core/utils/patch";
import {renderToElement} from "@web/core/utils/render";

export class FormToggleLegalTermsAction extends BuilderAction {
    static id = "formToggleLegalTerms";
    apply({editingElement: el}) {
        const legalTermsEl = el.querySelector(".s_website_form_legal");
        if (legalTermsEl) {
            legalTermsEl.remove();
        } else {
            const template = document.createElement("template");
            const labelWidth = el.querySelector(".s_website_form_label").style.width;
            template.content.append(
                renderToElement("website_form_require_legal.s_website_form_legal", {
                    labelWidth: labelWidth,
                    termsURL: "terms",
                })
            );
            const legal = template.content.firstElementChild;
            legal.setAttribute("contentEditable", true);

            const recaptchaEl = el.querySelector(".s_website_form_recaptcha");
            if (recaptchaEl) {
                recaptchaEl.before(legal);
            } else {
                const submitEl = el.querySelector(".s_website_form_submit");
                if (submitEl) {
                    submitEl.before(legal);
                }
            }
        }
    }

    isApplied({editingElement: el}) {
        return Boolean(el.querySelector(".s_website_form_legal"));
    }
}

patch(Plugin.prototype, {
    getResource(resourceId) {
        const resources = super.getResource(resourceId);
        if (resourceId && resourceId === "builder_actions") {
            return [...resources, {FormToggleLegalTerms: FormToggleLegalTermsAction}];
        }
        return resources;
    },
});
