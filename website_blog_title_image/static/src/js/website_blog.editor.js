$(document).ready(function() {
    "use strict";

    var website = openerp.website;
    
    if ($('.website_blog').length) {
        website.EditorBar.include({
            edit: function () {
                var self = this;
                this._super();
                $('body').on('click','#change_title_image',_.bind(this.change_title_image, self.rte.editor));
            },
            change_title_image: function() {
                var self  = this;
                var element = new CKEDITOR.dom.element(self.element.find('.title-image-storage').$[0]);
                var editor  = new website.editor.MediaDialog(self, element);
                
                $(document.body).on('media-saved', self, function (o) {
                    $('.title-image-storage').hide();
                });
                editor.appendTo('body');
            },
            save: function() {
                var res = this._super();
                openerp.jsonRpc("/blogpost/change_title_image", 'call', {
                    'post_id' : $('#blog_post_name').attr('data-oe-id'),
                    'image' : $('.title-image-storage').attr('src').replace(/url\(|\)|"|'/g,'')
                });
                return res;
            }
        });
    }
});
