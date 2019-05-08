/* © 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define('website_anchor_smooth_scroll.website_anchor_smooth_scroll', function (require) {

    "use strict";

    function website_anchor_smooth_scroll (event) {
        event.preventDefault();
        var target = $(event.currentTarget.hash);

        return $('html, body')
            .stop()
            .animate({
                'scrollTop': target.offset().top - 100,
            })
            .promise()
            .done(function () {
                history.pushState(null, document.title, event.target.hash);
            });
    }

    require('web.dom_ready');

    $("a[href^='#']:not([href=#])").on("click", website_anchor_smooth_scroll);

});
