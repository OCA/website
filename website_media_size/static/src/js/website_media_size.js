/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_media_size', function(require) {
"use strict";

    var MediaDialog = require('web_editor.widget').MediaDialog;
    var weContext = require("web_editor.context");
    var Widget = require('web.Widget');

    MediaDialog.include({
        xmlDependencies: MediaDialog.prototype.xmlDependencies.concat(
            ['/website_media_size/static/src/xml/website_media_size.xml']
        ),
        start: function() {
            var res = this._super.apply(this, arguments);
            this.search();
            return res;
        }
    });

    // ImageDialog of the web_editor.widget module is not available
    Widget.include({
        _rpc: function(params, options) {
            if (this.template === 'web_editor.dialog.image' &&
                params.model === 'ir.attachment' &&
                params.method === 'search_read') {
                params.kwargs.fields.push('file_size');
            }
            return this._super(params, options);
        }
    });
});
