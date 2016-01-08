/* © <YEAR(S)> <AUTHOR(S)>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
(function () {
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;
    website.add_template_file('/website_snippet_breadcrumb/static/src/xml/website_snippet_breadcrumb.editor.xml');

    website.snippet.options.website_snippet_breadcrumb = website.snippet.Option.extend({
        on_prompt: function () {
            var self = this;
            return new website.editor.WebsiteSnippetBreadcrumbSettingsDialog(self.$target).appendTo(document.body);
        },
        drop_and_build_snippet: function() {
            var self = this;
            this._super();
            this.on_prompt();
        },
        start : function () {
            var self = this;
            this.$el.find(".js_website_snippet_breadcrumb_settings").on("click", _.bind(this.on_prompt, this));
            this._super();
        },
        clean_for_save: function () {
            var include = 'False';
            if (this.$target.attr('data-include-self') == 'true'){
                include = 'True';
            }
            var revert = 'False';
            if(this.$target.attr('data-revert-order') == 'true'){
                revert = 'True';
            }
            this.$target.find('.parametricTemplate')
            .empty()
            .append(jQuery('<t />')
                    .attr('t-call', "website_breadcrumb.breadcrumb_generator")
                    .attr('t-ignore-branding', '1')
                    .append(
                        jQuery('<t />')
                            .attr('t-set', 'include_self')
                            .attr('t-value', include)
                            .attr('t-ignore-branding', '1'),
                        jQuery('<t />')
                            .attr('t-set', 'revert_order')
                            .attr('t-value', revert)
                            
                            .attr('t-ignore-branding', '1')
                    )
            );
        },
    });
    
    website.editor.WebsiteSnippetBreadcrumbSettingsDialog = website.editor.Dialog.extend({
        template: 'website_snippet_breadcrumb.editor.dialog.website_snippet_breadcrumb.settings',
        init: function (target) {
            this.$target = target;
            this._super(target);
        },
        start: function () {
            var self = this;
            self.$include_self_chk = self.$("input[id='include-self']");
            self.$revert_order_chk = self.$("input[id='revert-order']");
            return this._super().then(this.proxy('bind_data'));
        },

        save: function () {
            var self = this;
            self.$target.attr("data-include-self", self.$include_self_chk.prop('checked'));
            self.$target.attr("data-revert-order", self.$revert_order_chk.prop('checked'));
            return this._super();
        },

        bind_data: function () {
            var self = this;
            self.$include_self_chk.prop('checked', self.$target.attr('data-include-self') == 'true');
            self.$revert_order_chk.prop('checked', self.$target.attr('data-revert-order') == 'true');
        },
    });
})();


