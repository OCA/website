/* © 2015 Antiun Ingeniería, S.L.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

"use strict";
(function ($) {
    $(".cc-cookies .btn-primary").click(function(event){
        event.preventDefault();
        $.ajax($(event.target).attr("href"), {
            "complete": function(jqXHR, textStatus){
                $(event.target).closest(".cc-cookies").hide("fast");
            }
        });
    });
})(jQuery);
