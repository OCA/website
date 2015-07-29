(function () {
    'use strict';

    openerp.Tour.register({
        id:   'shop_buy_product_oca',
        name: "Try to buy products with one step checkout",
        path: '/shop',
        mode: 'test',
        steps: [
            {
                //step 0
                title:    "select iPad Mini",
                element: 'a[itemprop="name"][href*="ipad-mini"]',
            },
            {
                //step 1
                title:    "click on add to cart",
                element: '#add_to_cart',
            },
            {
                //step 2
                title:    "go to checkout",
                element: 'a[href="/shop/checkout"]',
            },
            {
                //step 3
                title:     "test with input error",
                element:   'form[action="/payment/transfer/feedback"] .btn[type="submit"]',
                onload: function (tour) {
                    $("input[name='phone']").val("");
                }
            },
            {
                //step 5
                title:     "test without input error",
                waitFor:   'div[id="osc_billing"] .has-error',
                element:   'form[action="/payment/transfer/feedback"] .btn[type="submit"]',
                onload: function (tour) {
                    if ($("input[name='name']").val() === "")
                        $("input[name='name']").val("website_sale-test-shoptest");
                    if ($("input[name='email']").val() === "")
                        $("input[name='email']").val("website_sale_test_shoptest@websitesaletest.optenerp.com");
                    $("input[name='phone']").val("123");
                    $("input[name='street']").val("xyz");
                    $("input[name='street_number']").val("123");
                    $("input[name='city']").val("Magdeburg");
                    $("input[name='zip']").val("39104");
                    $("select[name='country_id']").val("11");
                },
            },

            {
                //step 6
                title:     "finish",
                waitFor:   '.oe_website_sale:contains("Thank you for your order")',
            }
        ]
    });


}());
