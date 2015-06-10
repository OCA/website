/**
 * # -*- encoding: utf-8 -*-
 * ##############################################################################
 * #
 * #    OpenERP, Open Source Management Solution
 * #    This module copyright :
 * #        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
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
if (typeof jQuery === 'undefined') { throw new Error('POS Ticket Logo Addon requires jQuery') }

+function ($) {
    'use strict';

    openerp.pos_ticket_logo = function (instance, module) {
        var _t = instance.web._t,
            _lt = instance.web._lt;
        var QWeb = instance.web.qweb;

        instance.point_of_sale.PosModel = instance.point_of_sale.PosModel.extend({
            load_server_data: function(){
                var self = this;
                var loaded = instance.point_of_sale.PosModel.__super__.load_server_data.apply(this, arguments);
                $.when(loaded).then(function(){
                    self.company_logo.src = '/web/binary/image?model=res.company&id=' + self.company.id + '&field=logo';
                });
                return loaded;
            }
        });
    };

}(jQuery);
