(function() {
    "use strict";

    var website = openerp.website;
    var _t = openerp._t;

    website.layout.include({
        new_supplier_product: function() {
            website.prompt({
                id: "editor_new_product",
                window_title: _t("New Product"),
                input: "Product Name",
            }).then(function (name) {
                website.form('/shop/add_product', 'POST', {
                    name: name
                });
            });
        },
    });
})();