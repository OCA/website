/* Copyright 2015 Therp BV
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define('website_backed_views.backend_views', function(require)
{
    'use strict';
    
    var base = require('web_editor.base');
    var ActionManager = require('web.ActionManager');
    var WebClient = require('web.WebClient');
    var $ = require('$');
    
    base.ready().done(function() {
        var views = $('[data-website-backend-view-model]');
        if(!views.length)
        {
            return;
        }
        var backend = openerp.init();
        backend.client = new WebClient();
        backend.client.start().then(function()
        {
            _.each(views, function(view)
            {
                view = $(view);
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
                var action_manager = new ActionManager(backend.client);
                var view_manager = new backend.web.ViewManagerAction(
                        action_manager, action);
                view_manager.setElement(view);
                view_manager.renderElement();
                view_manager.start();
            });
        });
    });
});
