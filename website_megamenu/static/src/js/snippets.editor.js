// Copyright 2020 Odoo
// Copyright 2020 Tecnativa - Alexandre Díaz
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
odoo.define("website_megamenu.SnippetsEditor", function (require) {
    "use strict";

    var SnippetsEditor = require("web_editor.snippet.editor");

    SnippetsEditor.Class.include({
        /**
         * @private
         * @param {Boolean} show
         */
        toggleMegaMenuSnippets: function (show) {
            setTimeout(
                function () {
                    this._activateSnippet(false);
                }.bind(this)
            );
            this.$("#snippet_mega_menu").toggleClass("d-none", !show);
        },

        /**
         * Remove hidden drop zones. For example, mega menus
         *
         * @override
         */
        _activateInsertionZones: function () {
            this._super.apply(this, arguments);
            this.$editable.find(".oe_drop_zone:not(:visible)").remove();
        },
    });
});
