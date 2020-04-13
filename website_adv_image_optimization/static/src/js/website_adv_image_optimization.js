/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_adv_image_optimization', function (require) {
    "use strict";

    var MediaDialog = require('web_editor.widget').MediaDialog;
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;
    var csrf_token = core.csrf_token;

    var AdvancedOptimizationDialog = Dialog.extend({
        events: {
            'change input[name="width"],input[name="height"]': 'remain_ratio',
        },
        init: function (parent, attachment_id, attachment_src) {
            this.applied = $.Deferred();
            this.attachment_id = attachment_id;
            this.attachment_src = attachment_src;
            this._super(parent, {
                'dialogClass': 'o_advanced_optimization_dialog',
                'title': _t('Advanced Optimization (for images)'),
                '$content': $(qweb
                    .render(
                        'website_adv_image_optimization' +
                        '.AdvancedOptimizationDialog'
                    )
                ),
                'buttons': [
                    {
                        text: _t("Apply"),
                        classes: "btn-primary",
                        click: this.apply,
                    },
                    {text: _t("Cancel"), close: true},
                ],
            });
            this.set_defaults().done(function (dimensions) {
                this.ratio = dimensions[0] / dimensions[1];
            }.bind(this));
        },
        set_defaults: function () {
            return this.get_dimensions().done(function (dimensions) {
                this.$('input[name="width"]').val(dimensions[0]);
                this.$('input[name="height"]').val(dimensions[1]);
            }.bind(this));
        },
        get_dimensions: function () {
            var done = $.Deferred();
            var img = new Image();
            img.onload = function () {
                done.resolve([this.width, this.height]);
            };
            img.src = this.attachment_src;
            return done.promise();
        },
        apply: function () {
            return $.ajax({
                url: '/website_adv_image_optimization/attachment/optimize',
                method: 'POST',
                data: {
                    attachment_id: this.attachment_id,
                    quality: this.$('input[name="quality"]').val(),
                    width: this.$('input[name="width"]').val(),
                    height: this.$('input[name="height"]').val(),
                    csrf_token: csrf_token,
                },
            }).done(function () {
                this.applied.resolve();
            }.bind(this));
        },
        remain_ratio: function (e) {
            var $target = $(e.target);
            if ($target.attr('name') === 'width') {
                this.$('input[name="height"]')
                    .val(Math.round($target.val() / this.ratio));
            } else {
                this.$('input[name="width"]')
                    .val(Math.round($target.val() * this.ratio));
            }
        },
    });

    MediaDialog.include({
        xmlDependencies: MediaDialog.prototype.xmlDependencies.concat(
            [
                '/website_adv_image_optimization/' +
                'static/src/xml/website_adv_image_optimization.xml',
            ]
        ),
        events: _.extend({}, MediaDialog.prototype.events, {
            'click .o_existing_attachment_optimize': 'optimize_image',
        }),
        optimize_image: function (e) {
            var self = this;
            var attachment_id = parseInt($(e.target).attr('data-id'), 10);
            var record = self.imageDialog.records.filter(function (r) {
                return r.id === attachment_id;
            });
            if (record.length === 0 || record[0].type === 'url') {
                return;
            }

            var dialog = new AdvancedOptimizationDialog(
                this,
                attachment_id,
                record[0].src
            );
            dialog.open();
            dialog.applied.done(function () {
                dialog.close();
                self.imageDialog.search('').then(function () {
                    var record_data = self.imageDialog
                        .records.filter(function (r) {
                            return r.id === attachment_id;
                        });
                    self.imageDialog._toggleImage(record_data[0], false, true);
                });
            });
        },
    });

    return {
        'AdvancedOptimizationDialog': AdvancedOptimizationDialog,
    };
});
