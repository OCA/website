/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_snippet_preset', function (require) {
    'use strict';
    var snippet_editor = require('web_editor.snippet.editor');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var qweb = core.qweb;
    var _t = core._t;

    var OverwriteDialog = Dialog.extend({
        init: function (parent) {
            this.overwrite = $.Deferred();
            var options = {
                title: _t('Overwrite?'),
                $content: $(_t(
                    '<p>Preset with this name already exists.' +
                    'Do you want to overwrite it?</p>'
                )),
                buttons: [
                    {
                        text: _t("Overwrite"),
                        classes: 'btn-primary',
                        click: this.overwriteClicked.bind(this),
                    },
                    {
                        text: _t("No"),
                        classes: 'btn-default',
                        close: true,
                    },
                ],
            };
            return this._super(parent, options);
        },
        overwriteClicked: function () {
            this.overwrite.resolve();
            this.close();
        },
        open: function () {
            this._super.apply(this, arguments);
            return this.overwrite.promise();
        },
    });

    var EnterNameDialog = Dialog.extend({
        init: function (parent) {
            var options = {
                title: _t('Enter Name'),
                $content: $(qweb
                    .render('website_snippet_preset.EnterNameDialog', {
                        name: '',
                    })),
                buttons: [
                    {
                        text: _t("Save"),
                        classes: 'btn-primary',
                        click: this.saveClicked.bind(this),
                    },
                    {
                        text: _t("Cancel"),
                        classes: 'btn-default',
                        close: true,
                    },
                ],
            };
            return this._super(parent, options);
        },
        saveClicked: function () {
            this.trigger('save', this.$('input[name="name"]').val());
        },
    });
    snippet_editor.Editor.include({
        xmlDependencies: snippet_editor.Editor
            .prototype.xmlDependencies.concat(
                [
                    '/website_snippet_preset/static/' +
                    'src/xml/website_snippet_preset.xml',
                ]
            ),
        events: _.extend({}, snippet_editor.Editor.prototype.events, {
            'click .o_snippet_preset_save': 'saveCurrentPreset',
        }),
        start: function () {
            var res = this._super.apply(this, arguments);
            this.$preset_menu = this.$('.o_snippet_preset');
            this.$preset_load_menu = this.$('.o_snippet_preset_load');
            this.snippet_name = this.$target.data().name;
            if (!this.snippet_name) {
                this.$preset_menu.hide();
            }
            this.loadPresets().then(function (records) {
                this.renderPresets(records);
            }.bind(this));
            return res;
        },
        saveCurrentPreset: function () {
            var arch = this.$target[0].outerHTML;
            var snippet = this.snippet_name;

            var self = this;
            var dialog = new EnterNameDialog(this);
            dialog.on('save', this, function (name) {
                self.presetExists(snippet, name).done(function (exists) {
                    var save = function () {
                        self.savePreset(snippet, name, arch, exists);
                        dialog.close();
                    };
                    if (exists) {
                        new OverwriteDialog(dialog).open().done(save);
                    } else {
                        save();
                    }
                });
            });
            dialog.open();
        },
        presetExists: function (snippet, name) {
            var get_done = $.Deferred();
            this._rpc({
                model: 'snippet.preset',
                method: 'search_read',
                domain: [['snippet', '=', snippet], ['name', '=', name]],
            }).then(function (records) {
                get_done
                    .resolve(records.length === 0 ? false : records[0].id);
            });
            return get_done.promise();
        },
        deletePreset: function (id) {
            var self = this;
            return this._rpc({
                model: 'snippet.preset',
                method: 'unlink',
                args: [[id]],
            }).then(function () {
                self.loadPresets().then(function (records) {
                    self.renderPresets(records);
                });
            });
        },
        savePreset: function (snippet, name, arch, id) {
            var self = this;
            var save = null;
            if (id) {
                save = this._rpc({
                    model: 'snippet.preset',
                    method: 'write',
                    args: [[id], {arch: arch}],
                });
            } else {
                save = this._rpc({
                    model: 'snippet.preset',
                    method: 'create',
                    args: [{arch: arch, name: name, snippet: snippet}],
                });
            }

            save.then(function () {
                self.loadPresets().then(function (records) {
                    self.renderPresets(records);
                });
            });
            return save;
        },
        loadPresets: function () {
            return this._rpc({
                model: 'snippet.preset',
                method: 'search_read',
                order: 'name asc',
                domain: [['snippet', '=', this.snippet_name]],
            });
        },
        renderPreset: function (record) {
            var self = this;
            var $item = $(qweb
                .render('website_snippet_preset.Item', {'record': record}));
            $item.data('record', record);
            $item.click(function () {
                self.applyPreset($(this).data('record').arch);
            });
            $item.find('i').click(function (e) {
                self.deletePreset($(this).closest('li').data('record').id);
                e.stopPropagation();
            });
            this.$preset_load_menu.append($item);
            return $item;
        },
        renderPresets: function (records) {
            this.$preset_load_menu.html('');
            for (var i in records) {
                this.renderPreset(records[i]);
            }
        },
        applyPreset: function (arch) {
            var $arch = $(arch);
            this.$target.html($arch.html());
            this.$target.attr('class', $arch.attr('class'));
            this.$target.attr('style', $arch.attr('style'));
            this.$target.closest('.o_editable').trigger('content_changed');
        },
    });

    return {
        'EnterNameDialog': EnterNameDialog,
        'OverwriteDialog': OverwriteDialog,
    };
});
