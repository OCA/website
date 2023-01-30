odoo.define(
    "website_snippet_openstreetmap.s_openstreetmap_options",
    function (require) {
        "use strict";

        const options = require("web_editor.snippets.options");
        const core = require("web.core");
        const _t = core._t;
        const generateOpenStreetMapLink =
            require("website_snippet_openstreetmap.utils").generateOpenStreetMapLink;

        options.registry.OpenStreetMap = options.Class.extend({
            // --------------------------------------------------------------------------
            // Options
            // --------------------------------------------------------------------------

            async selectDataAttribute(previewMode, widgetValue, params) {
                await this._super(previewMode, widgetValue, params);
                if (
                    ["mapAddress", "mapType", "mapZoom"].includes(params.attributeName)
                ) {
                    this._updateSource();
                }
            },

            /* eslint-disable  no-unused-vars */
            async showDescription(previewMode, widgetValue, params) {
                const descriptionEl = this.$target[0].querySelector(".description");
                if (widgetValue && !descriptionEl) {
                    this.$target.append(
                        $(`
                    <div class="description">
                        <font>${_t("Visit us:")}</font>
                        <span>${_t(
                            "Our office is open Monday – Friday 8:30 a.m. – 4:00 p.m."
                        )}</span>
                    </div>`)
                    );
                } else if (!widgetValue && descriptionEl) {
                    descriptionEl.remove();
                }
            },
            /* eslint-enable no-unused-vars */

            // --------------------------------------------------------------------------
            // Private
            // --------------------------------------------------------------------------

            /**
             * @override
             */
            _computeWidgetState(methodName, params) {
                if (methodName === "showDescription") {
                    return Boolean(this.$target[0].querySelector(".description"));
                }
                return this._super(methodName, params);
            },
            /**
             * @private
             */
            _updateSource() {
                const dataset = this.$target[0].dataset;
                const $embedded = this.$target.find(".s_openstreetmap_embedded");
                const $info = this.$target.find(".missing_option_warning");
                if (dataset.mapAddress) {
                    this._rpc({
                        method: "geo_find",
                        model: "base.geocoder",
                        args: [dataset.mapAddress],
                    }).then((res) => {
                        var url = generateOpenStreetMapLink(res, dataset);
                        if (url) {
                            if (url !== $embedded.attr("data")) {
                                $embedded.attr("data", url);
                            }
                            $embedded.removeClass("d-none");
                            $info.addClass("d-none");
                        } else {
                            $embedded.attr("data", "");
                            $embedded.addClass("d-none");
                            $info.removeClass("d-none");
                        }
                    });
                } else {
                    $embedded.attr("data", "");
                    $embedded.addClass("d-none");
                    $info.removeClass("d-none");
                }
            },
        });

        return {
            OpenStreetMap: options.registry.OpenStreetMap,
        };
    }
);
