/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_portal_purchase_product.tour", function (require) {
    "use strict";

    var Tour = require("web.Tour");
    var $ = require('$');

    function _$ (selector) {
        return $(selector, "form#supplier_product");
    }

    var result = {
        form_values: {
            "#name": "Product name",
            "#price": "15.0",
            "#description_sale": "Product description",
            "input[name^=supplierinfo_][name$=_min_qty]": "1",
            "input[name^=supplierinfo_][name$=_delay]": "2",
            "input[name^=supplierinfo_][name$=_price]": "10",
            "input[name=weight]": "0.4",
        },
        choose_categories: function () {
            var $all = _$("select[name=public_categ_ids] option");
            _$($all[0], $all[1]).prop("selected", true);
        },
        check_form: function () {
            for (var key in result.form_values) {
                result.check_single(
                    key,
                    _$(key).val(),
                    result.form_values[key]
                );
            }
            var $categories = _$("select[name=public_categ_ids]");
            result.check_single(
                $categories.selector,
                $categories.val(),
                result.choose_categories() || $categories.val()
            );
        },
        check_single: function (selector, current, expected) {
            if (current != expected) {
                throw "error: Expected '" + expected + "' in " + selector +
                    ", but found '" + current + "'.";
            }
        },
        fill_form: function () {
            for (var key in result.form_values) {
                _$(key).val(result.form_values[key]);
            }
        },
    };
    result.tour = {
        id: "website_portal_purchase_product_tour",
        name: "Use the product manager",
        path: "/my/purchase/products",
        mode: "test",
        steps: [
            {
                title: "Go to create a product",
                element: "a[href='/my/purchase/products/new']",
                waitFor: "a[href='/my/purchase/products/new']",
            },
            {
                title: "Fill new product",
                waitFor: "form#supplier_product button[type=submit]",
                onend: result.fill_form,
            },
            {
                title: "Create product",
                element: "button[type=submit]",
                waitFor: "button[type=submit]",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (!/\/new$/.test(location.pathname)) {
                        return "Check the product got created finely";
                    }
                },
            },
            {
                title: "Check the product got created finely",
                waitFor: ".fa-eye",
                onend: result.check_form,
            },
            {
                title: "Go back to list",
                element: "a[href='/my/purchase/products']",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (location.pathname.endsWith("/products")) {
                        return "Check the product got created finely";
                    }
                },
            },
            {
                title: "Check the product got created finely",
                element: "input[name=search]",
                sampleText: "wrong",
                waitFor: "td:contains('Product name')",
            },
            {
                title: "Send wrong query",
                element: ".fa-search",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (location.search.indexOf("search=wrong") != -1) {
                        return "Enter good search";
                    }
                },
            },
            {
                title: "Enter good search",
                element: "input[name=search]",
                sampleText: "product",
                waitNot: "td:contains('Product name')",
            },
            {
                title: "Send good query",
                element: ".fa-search",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (location.search.indexOf("search=product") != -1) {
                        return "Go to edit product";
                    }
                },
            },
            {
                title: "Go to edit product",
                element: "a:contains('Product name')",
                waitFor: "a:contains('Product name')",
            },
            {
                title: "Publish product",
                element: ".js_publish_btn:visible",
                waitFor: ".js_publish_btn:visible",
            },
            {
                title: "Change name",
                element: "input[name=name]",
                sampleText: "Changed name",
                waitFor: ".js_publish_btn.btn-success",
                waitNot: ".js_publish_btn.btn-danger",
            },
            {
                title: "Save changes",
                element: "button[type=submit]",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (!location.pathname.endsWith("/new")) {
                        return "Return to list after editing product";
                    }
                },
            },
            {
                title: "Return to list after editing product",
                element: "a[href='/my/purchase/products']",
                waitFor: "input[name=name][value='Changed name']",
                onload: function() {
                    // HACK https://github.com/odoo/odoo/issues/12961
                    if (location.pathname.endsWith("/products")) {
                        return "Disable product";
                    }
                },
            },
            {
                title: "Disable product",
                element: "tr:contains('Changed name') .fa-trash",
                waitFor: "tr:contains('Changed name') .fa-trash",
            },
            {
                title: "Product got disabled",
                waitFor: "a[href='/my/purchase/products/new']",
                waitNot: "table",
            },
        ],
    };

    Tour.register(result.tour);
    return result;
});
