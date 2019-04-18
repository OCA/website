/* Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
 * Copyright 2019 Tecnativa - Cristina Martin R.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_anchor.link_dialog", function (require) {
    "use strict";
    var widget = require("web_editor.widget");

    /**
     * Add anchor features to link dialog
     */
    widget.LinkDialog.include({
        xmlDependencies: widget.LinkDialog.prototype.xmlDependencies.concat(
            ['/website_snippet_anchor/static/src/xml/link_dialog.xml']
        ),

        /**
         * Know current anchors in this page.
         *
         * @returns {Array}
         * List of current anchors.
         */
        currentAnchors: function () {
            var anchors = [];
            $("#wrapwrap, #wrap, #wrap [id]").each(function () {
                anchors.push($(this).attr("id"));
            });
            return anchors;
        },
    });
});
