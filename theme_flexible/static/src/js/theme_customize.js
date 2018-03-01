/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('theme_flexible.theme_customize', function(require) {
    "use strict";
    var ThemeCustomizeDialog = require('website.theme');
    var ctx = require('web_editor.context');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var qweb = core.qweb;
    var _t = core._t;

    var SelectGoogleFontDialog = Dialog.extend({
        init: function(parent, api_key) {
            var self = this;
            self.select = $.Deferred();
            self.api_key = api_key;
            var options = {
                title: _t('Select Google Font'),
                $content: $(qweb.render('theme_flexible.SelectGoogleFont')),
                buttons: [
                    {text: _t("Select"), classes: 'btn-primary', click: this.selectClicked.bind(this) },
                    {text: _t("Cancel"), classes: 'btn-default', close: true}
                ]
            };
            return this._super(parent, options);
        },
        open: function() {
            this._super.apply(this, arguments);
            return this.select.promise();
        },
        willStart: function() {
            var self = this;
            var get_fonts = this.loadGoogleFonts().done(function(fonts) {
                self.fonts = fonts;
            });
            return $.when(this._super.apply(this, arguments), get_fonts);
        },
        loadGoogleFonts: function() {
            var self = this;
            var font_get = $.Deferred();
            $.get('https://www.googleapis.com/webfonts/v1/webfonts?key=' + self.api_key, function(fonts) {
                font_get.resolve(fonts.items);
            }).fail(function() {
                font_get.reject();
            });
            return font_get.promise();
        },
        start: function() {
            var res = this._super.apply(this, arguments);
            var self = this;
            var source = function(q, cb) {
                var reg = new RegExp(q, 'i');
                var matches = [];
                $.each(self.fonts, function(i, font) {
                    if (reg.test(font.family)) {
                        matches.push(font);
                    }
                });
                cb(matches);
            };

            this.$('input[name="font"]').typeahead({
                hint: true,
                highlight: true,
                minLength: 0
            }, {
                name: 'fonts',
                source: source,
                display: function(font) {
                    return font.family;
                }
            });
            this.$('input[name="font"]').bind('typeahead:select', function(ev, font) {
                self.$('select[name="variant"]').html('');
                $.each(font.variants, function(i, variant) {
                    self.$('select[name="variant"]').append(
                        $("<option></option>").attr('value', variant).html(variant)
                    );
                });
            });
            return res;
        },
        selectClicked: function() {
            var family = this.$('input[name="font"]').typeahead('val');
            var variant = this.$('select[name="variant"]').val();
            if (variant === null) {
                return;
            }
            var italic = variant.indexOf('italic') !== -1;
            var weight = 400;
            if (variant === 'regular' || variant === 'italic') {
                weight = 400;
            } else {
                weight = parseInt(variant.replace('italic', ''), 10);
            }

            this.select.resolve({
                family: family,
                weight: weight,
                italic: italic
            });
        }
    });

    ThemeCustomizeDialog.include({
        theme: null,
        website: null,
        xmlDependencies: ['/theme_flexible/static/src/xml/theme_customize.xml'],
        events: {
            'click .btn-apply': 'apply',
            'click .btn-close': 'close',
            'click .select-google-font': 'selectGoogleFont'
        },
        willStart: function() {
            var self = this;
            var website_id = ctx.get().website_id;
            var get_theme = $.Deferred();
            this._rpc({
                model: 'website',
                method: 'search_read',
                domain: [['id', '=', website_id]]
            }).then(function(website) {
                self.website = website[0];
                self._rpc({
                    model: 'theme.flexible',
                    method: 'search_read',
                    domain: [['id', '=', website[0].theme_flexible_id[0]]]
                }).then(function(theme) {
                    self.theme = theme[0];
                    get_theme.resolve();
                });
            });
            return $.when(this._super.apply(this, arguments), get_theme);
        },
        start: function() {
            var res = this._super.apply(this, arguments);
            this.set(this.theme);
            this.$('a[href="#tab-layout"]').click();
            return res;
        },
        set: function(theme) {
            for(var name in theme) {
                var input = this.$('input[name="' + name + '"], select[name="' + name + '"]');
                var type = input.attr('type') || 'select';
                switch(type) {
                    case 'select':
                        input.val(theme[name]);
                        break;

                    case 'checkbox':
                        input.prop('checked', theme[name]);
                        break;

                    default:
                        if(theme[name] === false) {
                            theme[name] = '';
                        }
                        if(input.parent().hasClass('colorpicker-component')) {
                            if(theme[name]) {
                                input.parent().colorpicker({'color': theme[name]});
                            } else {
                                input.parent().colorpicker();
                            }
                        } else {
                            input.val(theme[name]);
                        }
                        break;
                }
            }
        },
        get: function() {
            var values = {};
            this.$('input, select').each(function() {
                var type = $(this).attr('type') || 'select';
                switch(type) {
                    case 'checkbox':
                        values[$(this).attr('name')] = $(this).prop('checked');
                        break;

                    default:
                        values[$(this).attr('name')] = $(this).val();
                        break;
                }
            });
            return values;
        },
        apply: function(e) {
            var $btn = $(e.target);
            $btn.attr('disabled', true);
            $btn.html($('<i class="fa fa-cog fa-spin" />'));
            return this._rpc({
                model: 'theme.flexible',
                method: 'write',
                args: [[this.theme.id], this.get()]
            }).then(function() {
                var href = '/website/theme_customize_reload'+
                    '?href='+encodeURIComponent(window.location.href)+
                    '&enable='+encodeURIComponent([
                        'theme_flexible.assets_frontend_menu',
                        'theme_flexible.assets_frontend_colors',
                        'theme_flexible.assets_frontend_fonts',
                        'theme_flexible.assets_frontend_layout',
                        'theme_flexible.layout'
                    ])+
                    '&disable=';
                window.location.href = href;
            });
        },
        selectGoogleFont: function(e) {
            var self = this;
            if (!self.website.google_font_api_key) {
                return Dialog.alert(this, '', {
                    $content: $(qweb.render('theme_flexible.NoGoogleAPIKey'))
                });
            }
            var $btn = $(e.currentTarget);
            var type = $btn.attr('data-type');
            var dialog = new SelectGoogleFontDialog(this, self.website.google_font_api_key);
            dialog.open().done(function(res) {
                self.$('input[name="font_' + type + '"]').val(res.family);
                self.$('input[name="font_' + type + '_weight"]').val(res.weight);
                self.$('input[name="font_' + type + '_italic"]').prop('checked', res.italic);
                self.$('input[name="font_' + type + '_google"]').prop('checked', true);

                dialog.close();
            });
        }
    });

    return {
        'SelectGoogleFontDialog': SelectGoogleFontDialog
    };
});
