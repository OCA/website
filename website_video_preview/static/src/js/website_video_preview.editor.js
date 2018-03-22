odoo.define('website_video_preview.editor', function(require) {
    "use strict";

    var VideoDialog = require('web_editor.widget').VideoDialog;

    VideoDialog.include({
        save: function() {
            var res = this._super.apply(this, arguments);
            if (this.$content.attr('data-v')) {
                var $media = $(res);

                // Add preview
                var $play_button = $('<img class="play_button" src="/website_video_preview/static/src/img/yt_button.png"/>');
                var $preview_img = $('<img class="video_preview" />');
                $preview_img.attr('src', 'https://img.youtube.com/vi/' + this.$content.attr('data-v') + '/sddefault.jpg');
                $preview_img.attr('data-iframe-src', this.$content.attr('src'));

                $media.find('iframe').remove();
                $media.append($preview_img);
                $media.append($play_button);

                this.media = $media[0];
            }
            return res;
        },
        _createVideoNode: function(url, options) {
            var res = this._super(url, options);
            var ytRegExp = /^(?:(?:https?:)?\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
            var ytMatch = url.match(ytRegExp);
            if (ytMatch && ytMatch[1].length === 11) {
                res.$video.attr('data-v', ytMatch[1]);
            }
            return res;
        }
    });
});
