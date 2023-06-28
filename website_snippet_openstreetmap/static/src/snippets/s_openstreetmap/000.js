odoo.define("website_snippet_openstreetmap.s_openstreetmap", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");
    const generateOpenStreetMapLink =
        require("website_snippet_openstreetmap.utils").generateOpenStreetMapLink;

    const OpenStreetMapWidget = publicWidget.Widget.extend({
        selector: ".s_openstreetmap",
        disabledInEditableMode: false,

        /**
         * @override
         */
        start: function () {
            const $embedded = this.$target.find(".s_openstreetmap_embedded");
            const $info = this.$target.find(".missing_option_warning");
            if (!$embedded.attr("data") && this.el.dataset.mapAddress) {
                const dataset = this.el.dataset;
                this._rpc({
                    method: "geo_find",
                    model: "base.geocoder",
                    args: [dataset.mapAddress],
                }).then((res) => {
                    var url = generateOpenStreetMapLink(res, this.el.dataset);
                    $embedded.attr("data", url);
                    $embedded.removeClass("d-none");

                    if (url) {
                        $embedded.attr("data", url);
                        $embedded.removeClass("d-none");
                        $info.addClass("d-none");
                    }
                });
            }
        },
    });

    publicWidget.registry.follow = OpenStreetMapWidget;

    return OpenStreetMapWidget;
});
