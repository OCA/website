/* © 2015-2016 Odoo S.A.
 * © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define('website_portal', function(require) {
    'use strict';
    require('website.website');

    if(!$('.o_website_portal_details').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_website_portal_details'");
    }

    var state_options = $("select[name='state_id']:enabled option:not(:first)");
    $('.o_website_portal_details').on('change', "select[name='country_id']", function () {
        var select = $("select[name='state_id']");
        state_options.detach();
        var displayed_state = state_options.filter("[data-country_id="+($(this).val() || 0)+"]");
        var nb = displayed_state.appendTo(select).show().size();
        select.parent().toggle(nb>=1);
    });
    $('.o_website_portal_details').find("select[name='country_id']").change();
});
