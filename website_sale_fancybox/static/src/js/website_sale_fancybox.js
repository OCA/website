odoo.define("website_sale_fancybox.FancyBox", function(require) {
    "use strict";
    var sAnimation = require("website.content.snippets.animation");
    sAnimation.registry.WebsiteSale = sAnimation.registry.WebsiteSale.extend({
        _startZoom: function() {
            this._super.apply(this, arguments);
            const $carousel_items = $(
                '#product_detail[data-zoom="fancybox"] .carousel-item img'
            );
            if ($carousel_items.length > 0) {
                $carousel_items.each(function() {
                    $(this).wrap(
                        '<a href="{0}" class="o_wsfb_fancybox_item" data-fancybox="product_carousel_gallery"></a>'.replace(
                            "{0}",
                            $(this).attr("src")
                        )
                    );
                });
                const $fancybox = $('[data-fancybox="product_carousel_gallery"]');
                if ($fancybox.length > 0) {
                    $fancybox.fancybox({
                        buttons: ["zoom", "slideShow", "fullScreen", "close"],
                    });
                }
            }
        },
    });
});
