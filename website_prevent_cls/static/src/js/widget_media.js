odoo.define("website_prevent_cls.widget_media", function(require) {
    "use strict";

    var FileWidget = require("wysiwyg.widgets.media").FileWidget;

    FileWidget.include({
        _save: function() {
            var self = this;
            var res = this._super.apply(this, arguments);
            res.then(function() {
                // Add the dimensions here
                var $media = self.media;
                var img = self.selectedAttachments[0];
                if (img.image_width && img.image_height) {
                    $media.width = img.image_width;
                    $media.height = img.image_height;
                }
            });
            return res;
        },
    });
});
