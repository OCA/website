/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('website_media_size', function (require) {
    "use strict";

    var web_editor_widget = require('web_editor.widget');
    var ImageWidget = web_editor_widget.ImageWidget;

    ImageWidget.include({
        xmlDependencies: ImageWidget.prototype.xmlDependencies.concat(
            ['/website_media_size/static/src/xml/website_media_size.xml']
        ),
        _rpc: function (params, options) {
            if (params.model === 'ir.attachment' &&
                params.method === 'search_read') {
                params.kwargs.fields.push('file_size');
            }
            return this._super(params, options);
        },
    });
});
