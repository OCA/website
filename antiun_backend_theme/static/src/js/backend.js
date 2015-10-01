/**
 * # -*- encoding: utf-8 -*-
 * ##############################################################################
 * #
 * #    OpenERP, Open Source Management Solution
 * #    This module copyright :
 * #        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
 * #                 Endika Iglesias <endikaig@antiun.com>
 * #                 Antonio Espinosa <antonioea@antiun.com>
 * #
 * #    This program is free software: you can redistribute it and/or modify
 * #    it under the terms of the GNU Affero General Public License as
 * #    published by the Free Software Foundation, either version 3 of the
 * #    License, or (at your option) any later version.
 * #
 * #    This program is distributed in the hope that it will be useful,
 * #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 * #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * #    GNU Affero General Public License for more details.
 * #
 * #    You should have received a copy of the GNU Affero General Public License
 * #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * #
 * ##############################################################################
 */

// Check jQuery available
if (typeof jQuery === 'undefined') { throw new Error('Theme JavaScript requires jQuery') }

// Check jQuery UI available
// if (typeof jQuery.ui === 'undefined') { throw new Error('Theme JavaScript requires jQuery UI') }

// Check Bootstrap JS plugins available
// if (typeof jQuery.fn.alert === 'undefined') { throw new Error('Theme JavaScript requires Bootstrap Alert plugin') }

// Check Backbone available
// if (typeof Backbone === 'undefined') { throw new Error('Theme JavaScript requires Backbone') }


+function ($) {
    'use strict';

    // LIBRARY OR OBJECT CODE HERE


    // Called when the HTML-Document is loaded and the DOM is ready, even if all the graphics haven’t loaded yet
    $(document).ready(function() {

        // CODE HERE

    });

    // Called when the complete page is fully loaded, including all frames, objects and images
    $(window).load(function() {

        // CODE HERE

    });

    openerp.antiun_backend_theme = function(instance, local) {
        var _t = instance.web._t,
            _lt = instance.web._lt;
        var QWeb = instance.web.qweb;

        // Do not show company logo, show theme logo
        // instance.web.WebClient.include({
        //     update_logo: function() {
        //         var company = this.session.company_id;
        //         // var img = this.session.url('/web/binary/company_logo' + (company ? '?company=' + company : ''));
        //         // this.$('.oe_logo img').attr('src', '').attr('src', img);
        //         this.$('.oe_logo_edit').toggleClass('oe_logo_edit_admin', this.session.uid === 1);
        //     },
        // });
    }

}(jQuery);

