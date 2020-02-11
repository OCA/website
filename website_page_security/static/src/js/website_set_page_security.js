// -*- coding: utf-8 -*-
// © 2017 Therp BV <http://therp.nl>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('wnb_website.editor_set_page_security', function (require) {
    "use strict";
    var core = require('web.core');
    var website = require('website.website');
    var _t = core._t;
    var qweb = core.qweb;
    var ajax = require('web.ajax');
    var Model = require('web.Model');

    website.TopBar.include({
        events: _.extend({}, website.TopBar.prototype.events, {
            'click [data-action="set_page_security"]': 'set_page_security',
        }),
        set_page_security: function () {
            var _create_form = function (data) {
                var $group = this.$dialog.find("div.form-group");
                $group.removeClass("mb0");
                this.$dialog.find('input[type="text"]').hide();
                this.$dialog.find('label[for="page-name"]').hide();
                for (var index in data) {
                    if ({}.hasOwnProperty.call(data, index)) {
                        var $add = $(
                            '<div/>', {'class': 'form-group'}
                        ).append(
                            $(
                                '<span/>',
                                {'class': 'col-sm-offset-3 col-sm-9 text-left'}
                            ).append(
                                qweb.render('web_editor.components.switch',
                                    {id: index, label: data[index][0]})
                            )
                        );
                        $add.find('input').prop('checked', data[index][1] );
                        $group.after($add);
                    }
                }
            };
            website.prompt({
                id: "editor_set_page_security",
                window_title: _.str.sprintf(
                    _t("Set Page Security for %s"), $('title')[0].text),
                input: _.str.sprintf(
                    _t('Set the page security for %s'), $('title')[0].text),
                init: function () {
                    var self = this;
                    ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                        model:'res.groups',
                        method:'get_page_groups',
                        args:[],
                        kwargs:{page: $('html').data('view-xmlid')},
                    }).then(_create_form.bind(self));
                },
            }).then(function (val, field, $dialog) {
                var cbxs = $dialog.find(
                    "input[type='checkbox']").filter(":checked");
                var values = _.map(cbxs, function (element) {
                    return parseInt(element.id, 10);
                });
                var page_id = $('html').data(
                    'main-object').replace('ir.ui.view(', '').replace(',)', '');
                new Model('ir.ui.view').call('write', [
                    [parseInt(page_id, 10)],
                    {'page_permission_ids': [[6, 0, values]]},
                ]);
            });
        },
    });
});

