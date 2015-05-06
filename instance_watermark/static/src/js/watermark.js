/**
 * # -*- encoding: utf-8 -*-
 * ##############################################################################
 * #
 * #    OpenERP, Open Source Management Solution
 * #    This module copyright :
 * #        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
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
if (typeof jQuery === 'undefined') { throw new Error('Instance Watermark Addon requires jQuery') }

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

    openerp.instance_watermark = function(instance, local) {
        var _t = instance.web._t,
            _lt = instance.web._lt;
        var QWeb = instance.web.qweb;

        // Do not show company logo, show theme logo
        instance.web.WebClient.include({
            service_instance: '',
            init: function() {
                this._super.apply(this, arguments);
                var url = this.session.url('');
                // TODO : Read these regex from Odoo config
                var local = /(openerp|odoo)\.local\.net/i;
                var devel = /devel\.antiun\.net/i;
                var demo = /demo\.antiun\.net/i;
                if (local.test(url)) {this.service_instance = 'local';}
                if (devel.test(url)) {this.service_instance = 'devel';}
                if (demo.test(url)) {this.service_instance = 'demo';}
            },
            set_title: function(title) {
                if (this.service_instance) {
                    if (! $('.oe_logo span.instance').length) {
                        $('.oe_logo').append(
                            '<span class="instance ' +
                            this.service_instance + '">' +
                            this.service_instance.toUpperCase() +
                            '</span>');
                    }
                    if (title) {
                        title = this.service_instance.toUpperCase() + ' - ' + title;
                        arguments[0] = title
                    }
                }
                this._super.apply(this, arguments);
            },
        });
    }

}(jQuery);

