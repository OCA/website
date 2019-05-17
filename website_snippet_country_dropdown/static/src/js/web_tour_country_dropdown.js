odoo.define("website_snippet_country_dropdown.tour_demo_page", function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var country_code_test = 'ES';
    var vat_number_test = 'B01010101';

    tour.register("website_snippet_country_dropdown_tour_demo_page", {
        url: "/page/website_snippet_country_dropdown.demo_page",
        wait_for: base.ready(),
    }, [{
        content: "Click Button",
        trigger: '#btn_vat_code',
        run: "click",
    }, {
        content: "Select Country",
        trigger: '#' + country_code_test,
        run: "click",
    }, {
        content: "Insert text",
        trigger: '#no_country_field',
        run: "text " + vat_number_test,
    },
    {
        content: "Validate Text",
        trigger: '#no_country_field',
        run: function () {
            // This function allow to evaluate a hidden html element
            // Impossible to do it through trigger
            var complete_field = $("#complete_field").val();
            if (complete_field !== country_code_test + vat_number_test) {
                // Abort test if the value is wrong
                console.log("error");
            }

        },
    }]);
});
