function pos_with_tax_widgets(instance, module){ //module is instance.point_of_sale
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    module.ProductListWidget = module.PosBaseWidget.extend({
        template:'ProductListWidget',
        init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.model = options.model;
            this.productwidgets = [];
            this.weight = options.weight || 0;
            this.show_scale = options.show_scale || false;
            this.next_screen = options.next_screen || false;

            this.click_product_handler = function(event){
                var product = self.pos.db.get_product_by_id(this.dataset['productId']);
                options.click_product_action(product);
            };

            this.product_list = options.product_list || [];
            this.product_cache = new module.DomCache();
        },
        set_product_list: function(product_list){
            this.product_list = product_list;
            this.renderElement();
        },
        get_product_image_url: function(product){
            return window.location.origin + '/web/binary/image?model=product.product&field=image_medium&id='+product.id;
        },
        get_product_price_with_tax: function(product){
            var taxes_ids = product.taxes_id;
            var taxes =  this.pos.taxes;
            var product_taxes = [];
                _(taxes_ids).each(function(el){
                    product_taxes.push(_.detect(taxes, function(t){
                        return t.id === el;
                    }));
                });
            total_amount = 0;
            for(i=product_taxes.length;i--;){
                total_amount += product_taxes[i].amount;
            }
            product.price_base = parseFloat(product.price);
            product.price = parseFloat((product.list_price + (product.list_price * total_amount)).toFixed(2));
        },
        replace: function($target){
            this.renderElement();
            var target = $target[0];
            target.parentNode.replaceChild(this.el,target);
        },

        render_product: function(product){
            var cached = this.product_cache.get_node(product.id);
            if(!cached){
                var image_url = this.get_product_image_url(product);
                this.get_product_price_with_tax(product);

                var product_html = QWeb.render('Product',{
                        widget:  this,
                        product: product,
                        image_url: this.get_product_image_url(product),
                    });
                var product_node = document.createElement('div');
                product_node.innerHTML = product_html;
                product_node = product_node.childNodes[1];
                this.product_cache.cache_node(product.id,product_node);
                return product_node;
            }
            return cached;
        },

        renderElement: function() {
            var self = this;

            // this._super()
            var el_str  = openerp.qweb.render(this.template, {widget: this});
            var el_node = document.createElement('div');
                el_node.innerHTML = el_str;
                el_node = el_node.childNodes[1];

            if(this.el && this.el.parentNode){
                this.el.parentNode.replaceChild(el_node,this.el);
            }
            this.el = el_node;

            var list_container = el_node.querySelector('.product-list');
            for(var i = 0, len = this.product_list.length; i < len; i++){
                var product_node = this.render_product(this.product_list[i]);
                product_node.addEventListener('click',this.click_product_handler);
                list_container.appendChild(product_node);
            };
        },
    });
}
