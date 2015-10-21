/**
 * # -*- coding: utf-8 -*-
 * ##############################################################################
 * #
 * #    OpenERP, Open Source Management Solution
 * #    This module copyright :
 * #        (c) 2014-Today Trey, Kilobytes de Soluciones <www.trey.es>
 * #                 Jorge Camacho <jcamacho@trey.es>
 * #        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
 * #                 Antonio Espinosa <antonioea@antiun.com>
 * #                 Endika Iglesias <endikaig@antiun.com>
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
if (typeof jQuery === 'undefined') { throw new Error('Website CRM privacy policy addon requires jQuery') }

+function ($) {
    'use strict';

    $(document).ready(function() {
        var _t = openerp._t;

        // Validate form
        $('form[action="/crm/contactus"]').on('submit', function(e) {
            // Validate privacy_policy is checked
            if(!$('input[name="privacy_policy"]').is(':checked')) {
                e.preventDefault();  // Prevent form from submitting
                alert(_t('You must accept our Privacy Policy.'));
            }
        });

    });

}(jQuery);
