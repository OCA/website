$(document).ready(function() {
    "use strict";

    var website = openerp.website;

    if ($('.website_blog').length) {
        website.EditorBar.include({
            clean_bg : function(vHeight) {
                if (jQuery('.cover').length && jQuery('.js_smallheight').length)
                {
                  var vheight = 450;
                  jQuery('.cover').css({"background-image":'none', 'min-height': vHeight});
                }
                this._super().apply(this, arguments);
            },
            change_bg: function(vHeight) {
                var self  = this;
                this._super.apply(this, arguments);
                if ($('.cover').length && jQuery('.js_smallheight').length)
                {
                    $(document.body).on('media-saved', self, function () {
                        var url = $('.cover-storage').attr('src');
                        $('.js_fullheight').css({"background-image": !_.isUndefined(url) ? 'url(' + url + ')' : "", 'min-height': 450});
                    });
                }
            },
        });
    }
});
