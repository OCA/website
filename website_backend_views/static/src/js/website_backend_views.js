//-*- coding: utf-8 -*-
//############################################################################
//
//   OpenERP, Open Source Management Solution
//   This module copyright (C) 2015 Therp BV <http://therp.nl>.
//
//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU Affero General Public License as
//   published by the Free Software Foundation, either version 3 of the
//   License, or (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU Affero General Public License for more details.
//
//   You should have received a copy of the GNU Affero General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//############################################################################
(function()
{
    openerp.website.dom_ready.then(function()
    {
        var views = jQuery('[data-website-backend-view-model]');
        if(!views.length)
        {
            return;
        }
        var backend = openerp.init();
        backend.client = new backend.web.WebClient();
        backend.client.start().then(function()
        {
            views.each(function(i, view)
            {
                view = jQuery(view);
                var action = {
                    'type': 'ir.actions.act_window',
                    'res_model': view.data('website-backend-view-model'),
                    'res_id': view.data('website-backend-view-res-id'),
                    'views': [
                        [
                            view.data('website-backend-view-id'),
                            view.data('website-backend-view-type')
                        ]
                    ],
                    'domain': view.data('website-backend-view-domain') || [],
                };
                var action_manager = new backend.web.ActionManager(backend.client);
                var view_manager = new backend.web.ViewManagerAction(
                        action_manager, action);
                view_manager.setElement(view);
                view_manager.renderElement();
                view_manager.start();
            });
        });
    });
})()
