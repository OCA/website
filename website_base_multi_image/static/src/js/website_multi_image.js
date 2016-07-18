/* © 2016 Tecnativa, S.L.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("website_base_multi_image.images",
function(require){
"use strict";

var animation = require("web_editor.snippets.animation");
var core = require("web.core");
var Model = require("web.Model");
var Session = require("web.Session");
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
        this.$main_image = this.$("#main_image");
        this.$file_input = this.$("#file_input");
        this.$label_input = this.$(".image_upload");
        this.$file_input_multi = this.$("#file_input_multi");
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
    },
    image_preview: function(e){
        var image = e.target.files[0];
        var reader = new FileReader();
        var self = this;
        reader.onload = (function(file) {
           return function(e) {
                self.image_added_id++;
                self.notify_clear();
                if (self.image_duplicate(file.name)){
                    self.user_notify(_t('This image already exists'));
                    return false;
                };
                var $img = $(core.qweb.render(
                "website_base_multi_image.image_preview", {
                    'src': e.target.result,
                    'title': escape(file.name),
                }));
                var $img_thumb = $(core.qweb.render(
                "website_base_multi_image.image_preview_thumb", {
                    'src': e.target.result,
                    'title': escape(file.name),
                }));
                self.$image_preview_thumb.append($img_thumb);
                self.render_image_upload();
           };
        })(image);
        reader.readAsDataURL(image);
    },
    render_image_upload: function(){
        this.$file_input_multi.append(this.$file_input);
        this.$file_input.attr("name", "new_image_" + this.image_added_id.toString());
        this.$file_input.attr("id", "new_image_" + this.image_added_id.toString());
        this.$file_input = $(core.qweb.render("website_base_multi_image.image_upload", {}));
        this.$label_input.append(this.$file_input);
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
        self.$("#images_container").append($notify);

    },
    notify_clear: function(){
        self.$(".notify").remove();
    },
});

return animation.registry.website_base_multi_image;
});
