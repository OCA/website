/* Copyright 2012-Today Serpent Consulting Services PVT. LTD. (http://www.serpentcs.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("website_portal_address.website_portal_address", function (require) {
    "use strict";
    var ajax = require("web.ajax");
    $(document).ready(function () {
        var first_execution = true;

        $('input[type="radio"]').click(function () {
            if ($(this).attr("value") === "contact") {
                $(".contact_address_website").hide();
            } else {
                $(".contact_address_website").show();
            }
        });

        $('input[type="radio"]').each(function () {
            if ($(this).attr('checked') === 'checked') {
                $(this).click();
            }
        });

        $('#country_id').change(function () {
            var option_count = 0;
            $("#state_id option").each(function () {
                var country_id = parseInt($('#country_id').val());
                var state_country_id = parseInt($(this).val().split("-", 1));
                if (country_id == state_country_id) {
                    option_count++;
                    $(this).removeAttr("disabled").show();
                } else {
                    $(this).attr("disabled", "disabled").hide();
                }
            });
            // Ignore first execution, it's override t-att-selected
            if (first_execution) {
                first_execution = false;
            } else {
                $("#state_id").val($("#state_id option:first").val());
            }
            // Hide state part if empty
            if (option_count > 0) {
                $('#state_id').parent().show();
            } else {
                $('#state_id').parent().hide();
            }
        }).change();
    });

});
