odoo.define("product_attribute_description.product_attribute_description", function () {
    "use strict";

    $('[data-toggle="tooltip"]').tooltip("show").tooltip("hide");

    $("#description_tooltip").on({
        click: function () {
            $(this).tooltip("show");
        },
    });

    $("#description_tooltip").mouseover(function () {
        $(this).tooltip("show");
    });
});
