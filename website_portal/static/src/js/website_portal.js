(function() {
'use strict';

openerp.website.if_dom_contains('div.o_website_portal_details', function() {

    $('.o_website_portal_details').on('change', "select[name='country_id']", function () {
        var $select = $("select[name='state_id']");
        $select.find("option:not(:first)").hide();
        var nb = $select
            .find("option[data-country_id="+($(this).val() || 0)+"]")
            .show().size();
        $select.parent().toggle(nb > 1);
    });
    $('.o_website_portal_details').find("select[name='country_id']").change();

});

}());
