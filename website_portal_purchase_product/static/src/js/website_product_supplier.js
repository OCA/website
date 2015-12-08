/* © 2015 Antiun Ingeniería, S.L.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

(function () {
    'use strict';

    var website = openerp.website,
    qweb = openerp.qweb;
    qweb.add_template('/website_product_supplier/static/src/xml/website.product.supplier.xml');

    $(document).ready(function () {
        $('.a-submit').off('click').on('click', function () {
            $(this).closest('form').submit();
        });
        $('.btn-del-product').click(del_click);
    });

    function del_click(e){
        e.preventDefault();
        $('.info > *').remove();
        var self = this;
        var supplierinfo_id = $(this).attr('oe_model_id');
        openerp.jsonRpc('/my/supplier/product/delete', 'call', {
                'supplierinfo_id': supplierinfo_id
            })
            .then(function(result) {
                debugger;
                if (result==true){
                    location.reload(true);
                };
            })
            .fail(function(d, error){
                var $row = $(qweb.render("website.product.supplier.list.error", {
                    'error_name': error['data']['message'],
                }));
                debugger;
                $('.info').append($row);
            });
    };

})();
