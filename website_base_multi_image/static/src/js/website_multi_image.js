/* © 2016 Tecnativa, S.L.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("website_base_multi_image.images",
function(require){
"use strict";

var animation = require("web_editor.snippets.animation");
var core = require("web.core");
var Model = require("web.Model");
var session = require("web.session");

var _t = core._t;
var $ = require("$");

animation.registry.website_base_multi_image =
animation.Class.extend({
    selector: ".js_image_container",
    start: function (editable_mode) {
        if (editable_mode) {
            return;
        };
        this.$image_preview_thumb = this.$(".thumbnail-images");
        this.$file_input = this.$("#file_input");
        this.$label_input = this.$(".image_upload");
        this.$file_input_multi = this.$("#file_input_multi");
        this.$carousel_container = this.$(".carousel-inner")
        this.image_added_id = 0;
        core.qweb.add_template(
            "/website_base_multi_image/static" +
            "/src/xml/website_multi_image.xml");
        this.bind_events();
    },
    bind_events: function () {
        var this_ = this;
        this.$el.on("change", "#file_input", function (event) {
            return this_.image_preview(event);
        });
        this.$el.on("click", ".remove-image", function (event) {
            return this_.image_remove(event);
        });
        this.$el.on("click", ".make-main-image", function (event) {
            return this_.image_make_main(event);
        });
    },
    image_preview: function (event) {
        var image = event.target.files[0];
        var reader = new FileReader();
        reader.fileName = image.name;
        reader.onload = $.proxy(this.reader_load, this);
        reader.readAsDataURL(image);
    },
    reader_load: function (event) {
        var filename = event.target.fileName;
        this.image_added_id++;
        this.notify_clear();
        if (this.image_duplicate(filename)){
            this.user_notify(_t('This image already exists'));
            return false;
        };
        var $img = $(core.qweb.render(
        "website_base_multi_image.image_preview", {
            'src': event.target.result,
            'title': escape(filename),
        }));
        var $img_thumb = $(core.qweb.render(
        "website_base_multi_image.image_preview_thumb", {
            'src': event.target.result,
            'title': escape(filename),
        }));
        this.$image_preview_thumb.append($img_thumb);
        this.render_image_upload();
    },
    render_image_upload: function(){
        this.$file_input_multi.append(this.$file_input);
        this.$file_input.attr("name", "new_image_" + this.image_added_id.toString());
        this.$file_input.attr("id", "new_image_" + this.image_added_id.toString());
        this.$file_input = $(core.qweb.render("website_base_multi_image.image_upload", {}));
        this.$label_input.append(this.$file_input);
    },
    image_remove: function(e){
        e.stopPropagation();
        var self = this;
        self.notify_clear();
        var $a = $(e.target);
        var id = parseInt($a.data('id'), 10);
        var Images = new Model('base_multi_image.image');
        Images.call('unlink', [id]).then(function(result){
            if (result){
                var $image_li = $a.closest('li');
                self.$carousel_container.find("div[slide-to=" + $image_li.data('slide-to') +"]").empty();
                $image_li.remove();
                return;
            } else {
                self.user_notify({'error': _t('Failed to remove image')});
            };
        })
    },
    image_make_main: function(e){
        var self = this;
        self.notify_clear();
        var $a = $(e.target);
        var id = parseInt($a.data('id'), 10);
        var Images = new Model('base_multi_image.image');
        Images.call('search', [[
            ['owner_model', '=', $a.data('owner_model')],
            ['owner_id', '=', $a.data('owner_id')]]])
        .then(function (images) {
            var order_images = [id];
            _.each(images, function (image) {
                if (!order_images.includes(image)){
                    order_images.push(image);
                };
            });
            self.reorder_images(order_images, $a);
        });
    },
    reorder_images: function(image_ids, target){
        session.rpc('/web/dataset/resequence', {
            model: 'base_multi_image.image',
            ids: image_ids,
            }).then(function (result) {
                var $main_image_thumb = self.$('a.fa-star');
                $main_image_thumb.removeClass('fa-star');
                $main_image_thumb.addClass('fa-star-o');
                target.removeClass('fa-star-o');
                target.addClass('fa-star');
        }, function () {
            self.user_notify({'error': _t('Failed to set main image')});
        });
    },
    image_duplicate: function(image_name){
        var duplicate = this.$("div[data-image_name='"+ image_name +"']");
        if (duplicate.length > 0){
            return true;
        }else{
          return false;
        };
    },
    user_notify: function(msg){
        var $notify = $(core.qweb.render(
        "website_base_multi_image.notify", {
            'description': msg,
        }));
        self.$("#images_container").prepend($notify);

    },
    notify_clear: function(){
        self.$(".notify").remove();
    },
});

return animation.registry.website_base_multi_image;
});
