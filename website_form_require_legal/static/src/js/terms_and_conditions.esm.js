/** @odoo-module **/

import {Component} from "@odoo/owl";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TermsAndConditionsCheckbox = publicWidget.Widget.extend({
    selector: 'div[name="website_form_terms_and_conditions"]',
    events: {
        "change #website_form_terms_and_conditions_input": "_onClickCheckbox",
    },

    async start() {
        this.checkbox = this.el.querySelector(
            "#website_form_terms_and_conditions_input"
        );
        Component.env.bus.trigger("enableSubmitButton");
        return this._super(...arguments);
    },
    _onClickCheckbox() {
        if (this.checkbox.checked) {
            Component.env.bus.trigger("enableSubmitButton");
        } else {
            Component.env.bus.trigger("disableSubmitButton");
        }
    },
});

export default publicWidget.registry.TermsAndConditionsCheckbox;
