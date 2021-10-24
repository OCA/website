odoo.define("website_critical_css.page_properties", function(require) {
    "use strict";

    var contentMenu = require("website.contentMenu");
    var PagePropertiesDialog = contentMenu.PagePropertiesDialog;

    PagePropertiesDialog.include({
        xmlDependencies: PagePropertiesDialog.prototype.xmlDependencies.concat([
            "/website_critical_css/static/src/xml/page_properties.xml",
        ]),

        save: function() {
            var values = {
                critical_css: this.$("#critical_css").val(),
            };
            this._rpc({
                model: "website.page",
                method: "write",
                args: [[this.page_id], values],
            });

            return this._super.apply(this, arguments);
        },
    });
});
