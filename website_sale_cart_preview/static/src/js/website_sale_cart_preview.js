$(document).ready(function() {
    var _t = openerp._t;
    var shopping_cart_link = $('ul#top_menu li a[href^="/shop/cart"]');
    var shopping_cart_link_counter;

    shopping_cart_link.popover({
        trigger: 'manual',
        animation: true,
        html: true,
        title: function () {
            return _t("My Cart");
        },
        container: 'body',
        placement: 'auto',
        template: '<div class="popover mycart-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
    }).on("mouseenter",function () {
        var self = this;
        clearTimeout(shopping_cart_link_counter);
        shopping_cart_link.not(self).popover('hide');
        shopping_cart_link_counter = setTimeout(function(){
            if($(self).is(':hover') && !$(".mycart-popover:visible").length)
            {
                $.get("/shop/cart", {'type': 'popover'})
                    .then(function (data) {
                        $(self).data("bs.popover").options.content =  data;
                        $(self).popover("show");
                        $(".popover").on("mouseleave", function () {
                            $(self).trigger('mouseleave');
                        });
                    });
            }
        }, 100);
    }).on("mouseleave", function () {
        var self = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                if(!$(self).is(':hover'))
                {
                   $(self).popover('hide');
                }
            }
        }, 1000);
    });

});
