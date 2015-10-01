/**
 * -*- coding: utf-8 -*-
 * © 2014-2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
 *             Antonio Espinosa <antonioea@antiun.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

// Check jQuery available
if (typeof jQuery === 'undefined') {
    throw new Error('website_sale_categories_megamenu requires jQuery')
}

+function ($) {
    'use strict';

    // Called when the HTML-Document is loaded and the DOM is ready, even if
    // all the graphics haven’t loaded yet
    $(document).ready(function() {
        // Open submenu
        $('div > li > ul > li.has-children')
        .children('a')
        .on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            var selected = $(this);

            if(selected.next('ul').hasClass('is-hidden')) {
                // Desktop version only
                selected.addClass('selected')
                .next('ul').removeClass('is-hidden').end()
                .parent('.has-children').parent('ul').addClass('moves-out');

                selected.parent('.has-children')
                .siblings('.has-children').children('ul').addClass('is-hidden')
                .end().children('a').removeClass('selected');
            } else {
                selected.removeClass('selected')
                .next('ul').addClass('is-hidden').end()
                .parent('.has-children').parent('ul').removeClass('moves-out');
            }
        });

        // Submenu items - go back link
        $('.go-back').on('click', function(){
            event.preventDefault();
            event.stopPropagation();
            $(this).parent('ul').addClass('is-hidden')
            .parent('.has-children').parent('ul').removeClass('moves-out');
        });
    });
}(jQuery);
