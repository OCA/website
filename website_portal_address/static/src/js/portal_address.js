/* Copyright 2012-Today Serpent Consulting Services PVT. LTD. (http://www.serpentcs.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("website_portal_contact.tour", function (require) {
    "use strict";
    var ajax = require("web.ajax");
    $(document).ready(function() {
        $('input[type="radio"]').click(function() {
            if($(this).attr("value")=="contact") {
                $(".contact_address_website").addClass('hidden');
            }
            else {
                $(".contact_address_website").removeClass('hidden');
            }
        })
        $('input[type="radio"]').each(function() {
            if($(this).attr('checked') == 'checked') {
                $(this).click();
            }
        })
    });
});
