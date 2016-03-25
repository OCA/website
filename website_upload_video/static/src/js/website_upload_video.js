(function () {
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;
    
    website.add_template_file('/website_upload_video/static/src/xml/website_upload_video.xml');
    
    website.editor.VideoDialog.include({
        events: _.extend({}, website.editor.VideoDialog.prototype.events, {
            'click .o_website_upload_video_btn': function (e) {
                e.preventDefault();
                var filepicker = this.$el.find('input[type=file]');
                if (!_.isEmpty(filepicker)){
                    filepicker[0].click();
                }
                this.hideMessage();
                return false;
            },
            'change input[type=file]': 'video_selected'
        }),
        video_selected: function(e) {
            var self = this;
            var $input = $(e.target);
            var $form = $input.parent();
            self.toggleButton();
            window['video_upload_callback'] = function(id) {
                self.set('attachment_id', id);
                delete window['video_upload_callback'];
                self.toggleButton();
                self.showMessage();
            }
            $form.submit();
        },
        showMessage: function() {
            var span = this.$el.find('.o_website_upload_success');
            span.removeClass('hidden');
            span.addClass('show');
        },
        hideMessage: function() {
            var span = this.$el.find('.o_website_upload_success');
            span.removeClass('show');
            span.addClass('hidden');
        },
        toggleButton: function() {
            var btn = this.$el.find('.o_website_upload_video_btn');
            if(btn.hasClass('disabled')) {
                btn.removeClass('disabled').html(_t('Upload a video from your computer'));
            } else {
                btn.addClass('disabled', 'disabled').html(_t('Uploading...'));
            }
        },
        save: function() {
            this._super();
            if(this.get('attachment_id') != null) {
                var $video = $(
                    '<video width="100%" height="100%" controls>' +
                        '<source src="/web/binary/saveas?model=ir.attachment&field=datas&id='+this.get('attachment_id')+'" type="video/mp4">' + 
                    '</video>'
                );
                $(this.media.$).replaceWith($video);
                this.media.$ = $video[0];
            }
        }
    });
    
})();
