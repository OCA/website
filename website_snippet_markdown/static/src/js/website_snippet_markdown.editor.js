odoo.define('website_snippet_markdown.editor', function(require){
"use strict";
    var options = require('web_editor.snippets.options');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;
    var qweb  = core.qweb;

    qweb.add_template('/website_snippet_markdown/static/src/xml/website_snippet_markdown.xml');

    var MarkdownDialog = Dialog.extend({
        template: 'website_snippet_markdown.dialog',
        init: function(html) {
            var self = this;
            this.content = html;
            this.html_parsed = this.parseHtml(html);
            return this._super(null, {
                'title': _t('Change Content'),
                 'buttons': [{'text': _t('Save'), 'close': true, 'click': _.bind(this.save, this)}]
            });
        },
        parseHtml(html) {
            var self = this;
            var und = new upndown();
            var content_parsed = $.Deferred();
            und.convert(html, function(err, markdown) {
                if (err) {
                    content_parsed.reject(err);
                }
                else {
                    content_parsed.resolve(markdown);
                }
            });
            return content_parsed;
        },
        start: function() {
            var self = this;
            var res = this._super.apply(this, arguments);

            var md = markdownit();
            var $textarea = this.$el.find('textarea');
            this._opened.done(function() {
                $textarea.markdown({
                    autofocus: true,
                    savable: false,
                    iconlibrary: 'fa',
                    onShow: function(e) {
                        self.html_parsed.done(function(markdown) {
                            e.setContent(markdown);
                        });
                    },
                    onChange: function(e) {
                        self.content = md.render(e.getContent());
                    },
                    onPreview: function(e) {
                        return md.render(e.getContent());
                    }
                });
            });
            return res;
        },
        save: function() {
            this.trigger("saved", this.content);
        }
    });

    options.registry.markdown = options.Class.extend({
        start: function() {
            // Don't use the default handling of option
            this.$el.on('click', _.bind(this.open_form, this));
            return this._super.apply(this, arguments);
        },
        open_form: function() {
            var editor = new MarkdownDialog(this.$target[0].innerHTML);
            editor.open();
            editor.on('saved', this, this.update_content);
        },
        update_content: function(html) {
            this.$target.html(html);
        }
    });

});