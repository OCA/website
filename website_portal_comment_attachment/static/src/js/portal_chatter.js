odoo.define('website_portal_comment_attachment.chatter', function (require) {
    'use strict';
    var core = require('web.core');
    var ajax = require('web.ajax');
    var PortalChatter = require('portal.chatter').PortalChatter;

    PortalChatter.include({
        _loadTemplates: function(){
            ajax.loadXML('/website_portal_comment_attachment/static/src/xml/portal_chatter.xml', core.qweb);
            return this._super.apply(this, arguments);
        },
        _onClickAttachmentsAdd: function(){
            var input = $('#chatter_attachment');
            $(input).trigger('click');
        },
        _onChatterAttachmentChange: function(){
            var list = $('#chatter_attachment_list');
            var btn = $('.o_portal_chatter_attachments_add');
            var input = $('#chatter_attachment');

            var abort = function () {
                input[0].value = "";
                input.trigger('change');
            };

            list.empty();
            btn.removeClass('d-none');
            for (var i=0; i<input[0].files.length; i++) {
                var fileindicator = document.createElement('i');
                fileindicator.className = 'fa-fw fa fa-file pr8';

                var abort_btn = document.createElement('button');
                abort_btn.className = 'btn';
                abort_btn.textContent = '×';
                abort_btn.title = 'Remove attachment';
                abort_btn.type = 'button';
                abort_btn.onclick = abort ;

                var item = document.createElement('li');
                item.className = 'list-inline-item';
                item.textContent = input[0].files[i].name;
                item.prepend(fileindicator);
                item.appendChild(abort_btn);

                list.append(item);
                btn.addClass('d-none');
            }
        },
        _onTextareaMessageComposerKeyup: function(ev){
            var btn_add = $('.o_portal_chatter_attachments_add');
            btn_add.prop("disabled", ev.target.value == "");
        },
        events: _.extend(
            {
                "click .o_portal_chatter_attachments_add": '_onClickAttachmentsAdd',
                "change #chatter_attachment": '_onChatterAttachmentChange',
                "keyup form.o_portal_chatter_composer_form textarea": '_onTextareaMessageComposerKeyup'
            },
            PortalChatter.prototype.events
        ),
        init: function () {
            this._super.apply(this, arguments);
        },
    });
});
