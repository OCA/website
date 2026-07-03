/* Copyright 2026 Hunki Enterprises BV */
import ticketDetailsWidget from "@website_event/js/website_event_ticket_details";

ticketDetailsWidget.include({
    start() {
        this.disableSubmitIfUnverified();
        return this._super(...arguments);
    },
    _onTicketQuantityChange() {
        this._super(...arguments);
        this.disableSubmitIfUnverified();
    },
    disableSubmitIfUnverified() {
        const altcha_widget = this.el.querySelector("altcha-widget");
        if (altcha_widget) {
            const button = this.el.querySelector("button.btn-primary");
            button.disabled = altcha_widget.getState() !== "verified";
        }
    },
});
