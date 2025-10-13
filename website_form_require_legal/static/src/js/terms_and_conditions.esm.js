import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";

export class TermsAndConditionsCheckbox extends Interaction {
    static selector = 'div[id="website_form_terms_and_conditions_div"]';
    dynamicContent = {
        "#website_form_terms_and_conditions_input": {
            "t-on-change": this._onClickCheckbox,
        },
    };

    async start() {
        this.checkbox = this.el.querySelector(
            "#website_form_terms_and_conditions_input"
        );
        this.env.bus.trigger("enableSubmitButton");
    }

    _onClickCheckbox() {
        if (this.checkbox.checked) {
            this.env.bus.trigger("enableSubmitButton");
        } else {
            this.env.bus.trigger("disableSubmitButton");
        }
    }
}

registry
    .category("public.interactions")
    .add("website_form_require_legal.terms_and_conditions", TermsAndConditionsCheckbox);
