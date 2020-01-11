odoo.define('website_img_dimension.tooltip', function(require) {
    "use strict";
    var Class = require('web.Class');
    var web_editor_base = require('web_editor.base');

    var TooltipManager = Class.extend({
        init: function() {
            var self = this;
            web_editor_base.ready().done(function() {
                $('#wrap').on('mouseenter', 'img', function() {
                    self.show_tooltip($(this));
                });

                $('#wrap').on('mouseleave', 'img', function() {
                    self.hide_tooltip($(this));
                });
            });
        },
        get_title: function($img) {
            return $img.width() + ' x ' + $img.height() + ' (' + $img[0].naturalWidth + ' x ' + $img[0].naturalHeight + ')';
        },
        show_tooltip: function($img) {
            $img.tooltip({
                title: this.get_title($img),
                trigger: 'manual',
                container: 'body'
            }).tooltip('show');
        },
        hide_tooltip: function($img) {
            $img.tooltip('destroy');
        }
    });

    var tooltip_manager = new TooltipManager();

    return {
        tooltip_manager: tooltip_manager,
        TooltipManager: TooltipManager
    };
});
