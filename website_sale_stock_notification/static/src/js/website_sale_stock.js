odoo.define("website_sale_stock_notification.VariantMix", function (require) {
    "use strict";

    var VariantMixin = require("sale.VariantMixin");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var QWeb = core.qweb;
    const {Markup} = require("web.utils");
    require("website_sale.website_sale");

    VariantMixin._onChangeCombinationStock = function (ev, $parent, combination) {
        let product_id = 0;
        // Needed for list view of variants
        if ($parent.find("input.product_id:checked").length) {
            product_id = $parent.find("input.product_id:checked").val();
        } else {
            product_id = $parent.find(".product_id").val();
        }
        const isMainProduct =
            combination.product_id &&
            ($parent.is(".js_main_product") || $parent.is(".main_product")) &&
            combination.product_id === Number(product_id);

        if (!this.isWebsite || !isMainProduct) {
            return;
        }

        const $addQtyInput = $parent.find('input[name="add_qty"]');
        let qty = $addQtyInput.val();

        $parent.find("#add_to_cart").removeClass("out_of_stock");
        $parent.find(".o_we_buy_now").removeClass("out_of_stock");
        if (
            combination.product_type === "product" &&
            !combination.allow_out_of_stock_order
        ) {
            combination.free_qty -= Number(combination.cart_qty);
            $addQtyInput.data("max", combination.free_qty || 1);
            if (combination.free_qty < 0) {
                combination.free_qty = 0;
            }
            if (qty > combination.free_qty) {
                qty = combination.free_qty || 1;
                $addQtyInput.val(qty);
            }
            if (combination.free_qty < 1) {
                $parent.find("#add_to_cart").addClass("disabled out_of_stock");
                $parent.find(".o_we_buy_now").addClass("disabled out_of_stock");
            }
        }
        var parent_xml = ajax.loadXML(
            "/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml",
            QWeb
        );
        var xml_load = $.when(
            parent_xml,
            ajax.loadXML(
                "/website_sale_stock_notification/static/src/xml/website_sale_stock.xml",
                QWeb
            )
        );
        xml_load.then(function () {
            $(".oe_website_sale")
                .find(".availability_message_" + combination.product_template)
                .remove();
            $(".oe_website_sale")
                .find(".custom_message_" + combination.product_template)
                .remove();
            combination.has_out_of_stock_message =
                $(combination.out_of_stock_message).text() !== "";
            combination.out_of_stock_message = Markup(combination.out_of_stock_message);
            var $message = $(
                QWeb.render("website_sale_stock.product_availability", combination)
            );
            const $custom_message = $(
                QWeb.render(
                    "website_sale_stock_notification.product_availability",
                    combination
                )
            );
            $("div.availability_messages").html($message);
            if (combination.show_availability && combination.custom_message) {
                $("div.custom_message").html($custom_message);
            }
        });
    };
    return VariantMixin;
});
