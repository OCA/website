/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_multi_theme.SwitchWebsiteMenu', function(require) {
'use strict';

    var navbar = require('website.navbar');
    var WebsiteNavbarActionWidget = navbar.WebsiteNavbarActionWidget;
    var rpc = require('web.rpc');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var qweb = core.qweb;
    var _t = core._t;

    var SwitchWebsiteMenu = WebsiteNavbarActionWidget.extend({
        xmlDependencies: ['/website_multi_theme/static/src/xml/switch_website_menu.xml'],
        events: _.extend({}, WebsiteNavbarActionWidget.prototype.events, {
            'click .dropdown-menu a': '_onWebsiteClicked'
        }),
        start: function () {
            var $current_website = this.$('.current-website');
            $current_website.html(window.location.hostname);

            var $dropdown_menu = this.$('.dropdown-menu');
            rpc.query({
                model: 'website',
                method: 'search_read',
                fields: ['domain', 'base_url']
            }).then(function (websites) {
                _.each(websites, function(website) {
                    $dropdown_menu.append(
                        $(qweb.render('website_multi_theme.SwitchWebsiteMenu', {
                            'website': website
                        }))
                    );
                });
            });

            return this._super.apply(this, arguments);
        },
        _onWebsiteClicked: function(e) {
            e.preventDefault();
            var $a = $(e.target);
            if ($a.attr('data-href')) {
                window.location = $a.attr('data-href');
            } else {
                Dialog.alert(this,
                    _t("To use this menu you'll have to set the `Base Url` " +
                       "of the website in the configuration menu (Website > Configuration > Websites).")
                );
            }
        }
    });

    navbar.websiteNavbarRegistry.add(SwitchWebsiteMenu, '#switch-website');

    return SwitchWebsiteMenu;
});
