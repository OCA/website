odoo.define('website_video_preview.frontend', function (require) {
    "use strict";

    var registry = require('website.content.snippets.animation').registry;

    registry.mediaVideo.include({
        events: {
            'click [data-iframe-src]': '_onPreviewClick',
            'click .play_button': '_onPlayButtonClick',
        },

        start: function () {
            var src = this.$target
                .find('img.video_preview').attr('data-iframe-src');
            if (!src) {
                return this._super.apply(this, arguments);
            }
            if (this.editableMode) {
                this.stopVideo();
            } else if (src.indexOf('autoplay=1') !== -1) {
                this.playVideo(
                    this.$target
                        .find('img.video_preview').attr('data-iframe-src'));
            }
        },

        _onPlayButtonClick: function (e) {
            var $img = $(e.currentTarget);
            var src = $img.parent()
                .find('[data-iframe-src]').attr('data-iframe-src');
            this.playVideo(src);
        },

        _onPreviewClick: function (e) {
            var $img = $(e.currentTarget);
            var src = $img.attr('data-iframe-src');
            this.playVideo(src);
        },

        playVideo: function (src) {
            var $iframe = $(
                "<iframe/>",
                {"class": "o_video_dialog_iframe", "frameborder": 0});
            $iframe.attr('src', src.replace('autoplay=0', 'autoplay=1'));
            this.$target.append($iframe);
            this.$target.find('img.video_preview').addClass('hidden');
            this.$target.find('img.play_button').addClass('hidden');
        },

        stopVideo: function () {
            this.$target.find('iframe').remove();
            this.$target.find('img.video_preview').removeClass('hidden');
            this.$target.find('img.play_button').removeClass('hidden');
        },
    });
});
