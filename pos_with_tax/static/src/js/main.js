openerp.pos_with_tax = function (instance) {
    var module = instance.point_of_sale;
	pos_with_tax_models(instance, module);
	pos_with_tax_widgets(instance, module);
};