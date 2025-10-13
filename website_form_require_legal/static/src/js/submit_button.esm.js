import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";

export class SubmitButton extends Interaction {
    static selector = ".s_website_form_send";

    async start() {
        this.SubmitButton = this.el;
        const legalDiv = document.querySelector(".s_website_form_legal");
        if (legalDiv) {
            this._disable();
        } else {
            this._enable();
        }
        this.env.bus.addEventListener("enableSubmitButton", this._enable.bind(this));
        this.env.bus.addEventListener("disableSubmitButton", this._disable.bind(this));
    }

    _enable() {
        this.SubmitButton.classList.remove("disabled");
    }

    _disable() {
        this.SubmitButton.classList.add("disabled");
    }
}

registry
    .category("public.interactions")
    .add("website_form_require_legal.submit_button", SubmitButton);
