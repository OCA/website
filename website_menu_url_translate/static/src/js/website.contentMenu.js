/*  Copyright 2017 initOS GmbH. <http://www.initos.com>
 *  Copyright 2017 GYB IT SOLUTIONS <http://www.gybitsolutions.com>
 *  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

(function () {
    'use strict';

    var website = openerp.website;
    var _t = openerp._t;

    website.contentMenu.EditMenuDialog.include({
		edit_menu: function (ev) {
            var self = this;
            var menu_id = $(ev.currentTarget).closest('[data-menu-id]').data('menu-id');
            var menu = self.flat[menu_id];
			this.elem = '';
            if (menu) {
                var dialog = new website.contentMenu.MenuEntryDialog(undefined, menu);
                dialog.on('update-menu', this, function (link) {
                    var id = link.shift();
                    var menu_obj = self.flat[id];
                    _.extend(menu_obj, {
                        name: link[2],
                        url: link[0],
                        new_window: link[1],
                    });
                    var $menu = self.$('[data-menu-id="' + id + '"]');
                    $menu.find('.js_menu_label').first().text(menu_obj.name);
                });
				dialog.appendTo(document.body);
				$('.modal-dialog').find('li.clearfix').after('<input type="checkbox" class="default_url"/>\
                                Use the page or URL of the default language.');
            } else {
                alert("Could not find menu entry");
            }
			$('.default_url').click(function(e) {
				if($(this). prop("checked") == true){
					this.elem = $('#s2id_link-page a').children().clone();
					openerp.jsonRpc("/defaulturl", 'call', {'menu_id': menu_id}).done(function (data) {
						if (data){
							$('#link-external').val('');
							$('#link-external').val(data);
							$('#link-external').prop("readonly", true);
							$('#s2id_link-page a').empty();
							$('#s2id_link-page').attr('disabled',true);
							$('#s2id_link-page').removeClass('select2-container');
					   	}
					});
				} else {
					$('#link-external').prop("readonly", false);
					$('#s2id_link-page').removeAttr('disabled');
					$('#s2id_link-page').addClass('select2-container');
					this.elem.appendTo($('#s2id_link-page a'));
				}
			});
        },
	});

})();
