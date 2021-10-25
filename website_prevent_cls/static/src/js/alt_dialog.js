odoo.define("website_prevent_cls.alt_dialog", function(require) {
    "use strict";

    var AltDialog = require("wysiwyg.widgets.AltDialog");

    AltDialog.include({
        xmlDependencies: AltDialog.prototype.xmlDependencies.concat([
            "/website_prevent_cls/static/src/xml/alt_dialog.xml",
        ]),

        init: function(parent, options, media) {
            this._super.apply(this, arguments);
            if (media.width && media.height) {
                this.image_width = media.width;
                this.image_height = media.height;
            }
        },

        save: function() {
            var newWidth = this.$("#image_width").val();
            var newHeight = this.$("#image_height").val();
            $(this.media).attr("width", newWidth);
            $(this.media).attr("height", newHeight);
            return this._super.apply(this, arguments);
        },
    });
});
