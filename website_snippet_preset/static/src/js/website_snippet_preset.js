/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_snippet_preset', function (require) {
    'use strict';
    var editor = require('web_editor.snippet.editor');
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

    var ChoiceDialog = Dialog.extend({
        init: function (parent, snippetName) {
            this.snippetName = snippetName;

            var options = {
                title: _t('Choose preset to load...'),
                $content: $(qweb
                    .render('website_snippet_preset.ChoiceDialog', {
                        name: '',
                    })),
                buttons: [
                    {
                        text: _t("Cancel"),
                        classes: 'btn-default',
                        close: true,
                    },
                ],
            };
            return this._super(parent, options);
        },
        start: function () {
            var res = this._super.apply(this, arguments);
            this.$list = this.$el.find('.list-group');
            this.loadPresets().then(function (records) {
                this.renderPresets(records);
            }.bind(this));
            return res;
        },
        itemClicked: function (arch) {
            this.trigger('apply', arch);
            this.close();
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
        loadPresets: function () {
            return this._rpc({
                model: 'snippet.preset',
                method: 'search_read',
                order: 'name asc',
                domain: [['snippet', '=', this.snippetName]],
            });
        },
        renderPreset: function (record) {
            var self = this;
            var $item = $(qweb
                .render('website_snippet_preset.Item', {'record': record}));
            $item.data('record', record);
            $item.click(function () {
                self.itemClicked($(this).data('record').arch);
            });
            $item.find('.badge').click(function (e) {
                self.deletePreset($(this).closest('.list-group-item').data('record').id);
                e.stopPropagation();
            });
            this.$list.append($item);
            return $item;
        },
        renderPresets: function (records) {
            this.$list.html('');
            for (var i in records) {
                this.renderPreset(records[i]);
            }
        },
    });

    editor.Editor.include({
        xmlDependencies: editor.Editor
            .prototype.xmlDependencies.concat(
                [
                    '/website_snippet_preset/static/' +
                    'src/xml/website_snippet_preset.xml',
                ]
            ),
        _initializeOptions: function () {
            var res = this._super.apply(this, arguments);
            var $optionsSection = _.last(this._customize$Elements);
            var snippetName = this.$target.data().name;

            var $presetLoad = $optionsSection.find('.o_snippet_preset_load');
            $presetLoad.data('snippetName', snippetName);
            $presetLoad.click(this.loadPreset.bind(this));

            var $presetSave = $optionsSection.find('.o_snippet_preset_save');
            $presetSave.data('snippetName', snippetName);
            $presetSave.click(this.saveCurrentPreset.bind(this));

            if (!snippetName) {
                $presetLoad.addClass('d-none');
                $presetSave.addClass('d-none');
            }
            return res;
        },
        loadPreset: function (event) {
            var $target = $(event.target);
            var snippetName = $target.data('snippetName');

            var self = this;
            var dialog = new ChoiceDialog(this, snippetName);
            dialog.on('apply', this, function (arch) {
                self.applyPreset(arch);
            });
            dialog.open();
        },
        saveCurrentPreset: function (event) {
            var arch = this.$target[0].outerHTML;
            var snippet = $(event.target).data('snippetName');

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
            return save;
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
        'ChoiceDialog': ChoiceDialog
    };
});
