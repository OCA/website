/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_media_size', function(require) {
    var MediaDialog = require('web_editor.widget').MediaDialog;
    var weContext = require("web_editor.context");

    MediaDialog.include({
        xmlDependencies: MediaDialog.prototype.xmlDependencies.concat(
            ['/website_media_size/static/src/xml/website_media_size.xml']
        ),
        start: function() {
            var res = this._super.apply(this, arguments);
            this.include_file_size(this.imageDialog);
            this.include_file_size(this.documentDialog);
            this.search(); // FIXME
            return res;
        },
        include_file_size: function(obj) {
            var self = this;
            // ImageDialog of the web_editor.widget module is not available
            obj.fetch_existing = function(needle) {
                var domain = [['res_model', '=', 'ir.ui.view']].concat(obj.domain);
                if (needle && needle.length) {
                    domain.push('|', ['datas_fname', 'ilike', needle], ['name', 'ilike', needle]);
                }
                return self._rpc({
                    model: 'ir.attachment',
                    method: 'search_read',
                    args: [],
                    kwargs: {
                        domain: domain,
                        fields: ['name', 'mimetype', 'checksum', 'url', 'type', 'file_size'],
                        order: [{name: 'id', asc: false}],
                        context: weContext.get(),
                    }
                }).then(obj.proxy('fetched_existing'));
            };
        }
    });
});
