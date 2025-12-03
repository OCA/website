import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.WebsiteSelect2 = publicWidget.Widget.extend({
    selector: "select:not(.select2-disable)",
    MIN_ITEMS: 6,
    DEFAULT_OPTIONS: {
        theme: "bootstrap-5",
    },
    start: function () {
        if (
            !this.$el.hasClass("select2-force") &&
            this.$el.find("option").length < this.MIN_ITEMS
        ) {
            return;
        }
        this.$el.select2(this._select2_options());
    },
    _select2_options: function () {
        return Object.assign(
            {},
            this.DEFAULT_OPTIONS,
            this.$el.data("select2-options") || {}
        );
    },
});
