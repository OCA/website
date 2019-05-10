odoo.define('website_video_preview.editor', function (require) {
    "use strict";

    var VideoDialog = require('web_editor.widget').VideoDialog;

    /**
     * Adds the ability to show a preview of the video
     * instead of loading the player.
     *
     * To extend this with other providers
     * you simply have to add a entry in video_preview e.g.::
     *
     *     this.video_preview.vim = {
     *         // The location of the image of the play button you want to show
     *         'button': '/website_video_preview/static/src/img/yt_button.png',
     *         // Provide a function that extracts the video ID from url
     *         'getVideoId': this._getYoutubeVideoId,
     *         // Provide a function that gets the preview image by video ID
     *         'getPreviewImage': this._getYoutubePreviewImage
     *     }
     */
    VideoDialog.include({
        video_review: null,

        /**
         * @class
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.video_preview = {
                'yt': {
                    "button": "/website_video_preview/" +
                        "static/src/img/yt_button.png",
                    'getVideoId': this._getYoutubeVideoId,
                    'getPreviewImage': this._getYoutubePreviewImage,
                },
            };
        },

        /**
         * @override
         */
        save: function () {
            var res = this._super.apply(this, arguments);
            var videoId = this.$content.attr('data-video-id');
            var type = this.$content.attr('data-video-type');
            if (videoId && type in this.video_preview) {

                // Build preview
                var $media = $(res);
                $media.find('iframe').remove();
                $media.append(this._createPreviewImageNode(type, videoId));
                $media.append(this._createPlayButtonNode(type));

                this.media = $media[0];
            }
            return res;
        },

        /**
         * Create the play button element (an image).
         *
         * @param {String} type The type of the video (e.g. yt, ins, vim)
         * @private
         * @returns {jQuery}
         */
        _createPlayButtonNode: function (type) {
            var meta = this.video_preview[type];
            var $play_button = $(
                "<img/>", {"class": "play_button", "src": meta.button});
            return $play_button;
        },

        /**
         * Create the preview image element.
         *
         * @param {String} type The type of the video (e.g. yt, ins, vim)
         * @param {String} id The ID of the video
         * @private
         * @returns {jQuery}
         */
        _createPreviewImageNode: function (type, id) {
            var meta = this.video_preview[type];
            var $preview_img = $('<img class="video_preview" />');
            $preview_img.attr('src', meta.getPreviewImage(id));
            $preview_img.attr('data-iframe-src', this.$content.attr('src'));
            return $preview_img;
        },

        /**
         * Get the Youtube preview image url by video ID.
         *
         * @param {String} id The ID of the video
         * @private
         * @returns {String}
         */
        _getYoutubePreviewImage: function (id) {
            return 'https://img.youtube.com/vi/' + id + '/0.jpg';
        },

        /**
         * Extracts the Youtube video ID from an url.
         *
         * @param {String} url The URL to the Youtube video
         * @private
         * @returns {String} The video ID
         */
        _getYoutubeVideoId: function (url) {
            var regex = new RegExp(["^(?:(?:https?:)?//)?(?:www.)?",
                "(?:youtu.be/|youtube.com/(?:embed/|v/|",
                "watch?v=|watch?.+&v=))((w|-){11})(?:S+)?$"].join(""));
            var matches = url.match(regex);
            return matches[1];
        },

        /**
         * @override
         */
        _createVideoNode: function (url, options) {
            var res = this._super(url, options);

            if (res.type in this.video_preview) {
                var meta = this.video_preview[res.type];
                res.$video.attr('data-video-type', res.type);
                res.$video.attr('data-video-id', meta.getVideoId(url));
            }
            return res;
        },
    });
});
