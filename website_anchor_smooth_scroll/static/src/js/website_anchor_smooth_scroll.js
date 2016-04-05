/* © 2016 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

"use strict";

function website_anchor_smooth_scroll(event) {
    event.preventDefault();

    var target = $(event.target.hash);

    return $('html, body')
    .stop()
    .animate({
        'scrollTop': target.offset().top - 100
    })
    .promise()
    .done(function(element) {
        history.pushState(null, document.title, event.target.hash);
    });
}

(function ($) {
    // Apply to all links that start with `#`
    $("a[href^='#']").live("click", website_anchor_smooth_scroll);
})(jQuery);
