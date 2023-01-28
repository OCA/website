odoo.define("website_snippet_dynamic_link.s_dynamic_link", function (require) {
    "use strict";

    var core = require("web.core");
    var rpc = require("web.rpc");
    const publicWidget = require("web.public.widget");
    const QWeb = core.qweb;

    const DynamicLinkWidget = publicWidget.Widget.extend({
        selector: ".s_dynamic_link",
        xmlDependencies: [
            "/website_snippet_dynamic_link/static/src/snippets/s_dynamic_link/000.xml",
        ],
        disabledInEditableMode: false,

        /**
         * @override
         */
        start: function () {
            var container = this.$(".s_dynamic_link_container");
            var parent = container[0].parentElement;

            var imageLayout = parent.getAttribute("data-option-image-layout");
            var imageSize = parent.getAttribute("data-option-image-size");

            var optionClasses = [];

            if (imageLayout === "optionRounded") optionClasses.push("rounded");
            else if (imageLayout === "optionCircle")
                optionClasses.push("rounded-circle");
            else if (imageLayout === "optionShadow") optionClasses.push("shadow");
            else if (imageLayout === "optionThumbnail")
                optionClasses.push("img-thumbnail");
            else optionClasses.push("rounded");

            if (imageSize === "option1") optionClasses.push("img-1x");
            else if (imageSize === "option2") optionClasses.push("img-2x");
            else if (imageSize === "option3") optionClasses.push("img-3x");
            else if (imageSize === "option4") optionClasses.push("img-4x");
            else if (imageSize === "option5") optionClasses.push("img-5x");
            else optionClasses.push("img-1x");

            optionClasses = optionClasses.join(" ");

            container[0].innerHTML = "";
            var website_id = this._getContext().website_id;
            var def = rpc
                .query({
                    model: "website.dynamic.link",
                    method: "search_read",
                    args: [
                        [
                            "|",
                            ["website_id", "=", null],
                            ["website_id", "=", website_id],
                        ],
                        ["id", "name", "url"],
                    ],
                })
                .then(function (dynamic_link_records) {
                    if (dynamic_link_records.length === 0) {
                        container.append("No Dynamic Link to Show");
                    }
                    _.each(dynamic_link_records, function (record) {
                        var image_url =
                            "web/image?model=website.dynamic.link&id=" +
                            record.id.toString() +
                            "&field=icon";
                        container.append(
                            QWeb.render(
                                "website_snippet_dynamic_link.s_dynamic_link.dynamic_link_item",
                                {
                                    dynamic_link_url: record.url,
                                    dynamic_link_name: record.name,
                                    dynamic_link_image: image_url,
                                    option_classes: optionClasses,
                                }
                            )
                        );
                    });
                });
            return Promise.all([this._super.apply(this, arguments), def]);
        },

        /**
         * @override
         */
        destroy: function () {
            this._super.apply(this, arguments);
            var container = this.$(".s_dynamic_link_container")[0];
            container.innerHTML = "";
        },
    });

    publicWidget.registry.dynamicLink = DynamicLinkWidget;

    return DynamicLinkWidget;
});
