odoo.define("website_google_analytics_4.tracking", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");

    publicWidget.registry.websiteSaleTracking.include({
        /**
         * @override
         */
        start: function () {
            const self = this;
            if (this.$("div.oe_website_sale_tx_status_google4").length) {
                const orderID = this.$("div.oe_website_sale_tx_status_google4").data(
                    "order-id"
                );
                this._vpv("/stats/ecom/order_confirmed/" + orderID);
                this._rpc({
                    route: "/shop/tracking_last_order/",
                }).then(function (o) {
                    if (o.transaction) {
                        self._trackGA("event", "purchase", o.transaction);
                    }
                });
            }
            return this._super.apply(this, arguments);
        },
        _trackGA: function () {
            // eslint-disable-next-line no-empty-function
            const websiteGA = window.gtag || function () {};
            websiteGA.apply(this, arguments);
        },
    });
});
