/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_multi_theme.editor', function(require) {
'use strict';

    var contentMenu = require('website.contentMenu');
    var PagePropertiesDialog = contentMenu.PagePropertiesDialog;
    var core = require('web.core');
    var qweb = core.qweb;

    PagePropertiesDialog.include({
        xmlDependencies: PagePropertiesDialog.prototype.xmlDependencies.concat(
            ['/website_multi_theme/static/src/xml/page_properties_dialog.xml']
        ),
        willStart: function() {
            var self = this;
            var defs = [this._super.apply(this, arguments)];

            defs.push(this._rpc({
                model: 'website',
                method: 'search_read',
                fields: ['domain']
            }).then(function(websites) {
                self.websites = websites;
            }));

            defs.push(this._rpc({
                model: 'website.page',
                method: 'search_read',
                fields: ['website_ids'],
                domain: [['id', '=', self.page_id]]
            }).then(function(page) {
                self.website_ids = page[0].website_ids;
            }));

            return $.when.apply($, defs);
        },
        start: function() {
            var self = this;
            var res = this._super.apply(this, arguments);

            var $checkbox_container = this.$('#website_ids > div');

            _.each(this.websites, function(website) {
                $checkbox_container.append(qweb.render('website_multi_theme.WebsiteCheckbox', {
                    'id': website.id,
                    'domain': website.domain,
                    'checked': _.contains(self.website_ids, website.id)
                }));
            });

            return res;
        },
        save: function() {
            var website_ids = [];
            this.$('#website_ids input[type="checkbox"]:checked').each(function() {
                website_ids.push(parseInt($(this).attr('data-id'), 10));
            });

            this._rpc({
                model: 'website.page',
                method: 'write',
                args: [[this.page_id], { website_ids: [[6, 0, website_ids]] }]
            });

            return this._super.apply(this, arguments);
        }
    });
});
