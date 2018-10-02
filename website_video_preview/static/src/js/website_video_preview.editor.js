odoo.define('website_video_preview.editor', function(require) {
    "use strict";

    var VideoDialog = require('web_editor.widget').VideoDialog;

    VideoDialog.include({
        video_review: null,

        init: function() {
            this._super.apply(this, arguments);
            this.video_preview = {
                'yt': {
                    'button': '/website_video_preview/static/src/img/yt_button.png',
                    'getVideoId': this._getYoutubeVideoId,
                    'getPreviewImage': this._getYoutubePreviewImage
                }
            }
        },

        save: function() {
            var res = this._super.apply(this, arguments);
            var videoId = this.$content.attr('data-video-id');
            var type = this.$content.attr('data-video-type');
            if (videoId && type in this.video_preview) {
                console.log(this.video_preview);
                var meta = this.video_preview[type];

                // Build preview
                var $media = $(res);
                $media.find('iframe').remove();
                $media.append(this._createPreviewImageNode(type, videoId));
                $media.append(this._createPlayButtonNode(type));

                this.media = $media[0];
            }
            return res;
        },

        _createPlayButtonNode: function(type) {
            var meta = this.video_preview[type];
            var $play_button = $('<img class="play_button" src="' + meta.button + '"/>');
            return $play_button;
        },

        _createPreviewImageNode: function(type, id) {
            var meta = this.video_preview[type];
            var $preview_img = $('<img class="video_preview" />');
            $preview_img.attr('src', meta.getPreviewImage(id));
            $preview_img.attr('data-iframe-src', this.$content.attr('src'));
            return $preview_img;
        },

        _getYoutubePreviewImage: function(id) {
            return 'https://img.youtube.com/vi/' + id + '/sddefault.jpg';
        },

        _getYoutubeVideoId: function(url) {
            var regex = /^(?:(?:https?:)?\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
            var matches = url.match(regex);
            return matches[1];
        },

        _createVideoNode: function(url, options) {
            var res = this._super(url, options);

            if (res.type in this.video_preview) {
                var meta = this.video_preview[res.type];
                res.$video.attr('data-video-type', res.type);
                res.$video.attr('data-video-id', meta.getVideoId(url));
            }
            return res;
        }
    });
});
