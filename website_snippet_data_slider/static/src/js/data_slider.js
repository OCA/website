/* Copyright 2016 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */

odoo.define('website_snippet_data_slider', function(require){
  "use strict";
    
    var animation = require('web_editor.snippets.animation');
    
    var defaults = {
        lazyLoad: 'ondemand',
        slidesToShow: 5,
        slidesToScroll: 1,
        dots: true,
        infinite: true,
        speed: 500,
        arrows: true,
        autoplay: true,
        adaptiveHeight: false,
        variableWidth: false,
        autoplaySpeed: 3000,
        data_model: 'product.template',
        data_domain: [['website_published', '=', true]],
        data_image_field: 'image_medium',
        data_name_field: 'display_name',
        data_title: 'Featured Products',
        data_title_tag: 'h1',
        data_title_class: 'text-center',
        data_uri_field: 'website_url',
        data_container_width: '90%',
        data_limit: 10,
        prevArrow: '<a href="#" class="slider-arrow-left"><i class="fa fa-arrow-left fa-2x"></i></a>',
        nextArrow: '<a href="#" class="slider-arrow-right"><i class="fa fa-arrow-right fa-2x"></i></a>',
    };
    
    animation.registry.data_slider = animation.Class.extend({
        selector: ".o_data_slider",
        
        slickSetOption: function(event, key, val) {
            switch (val) {
                case 'true':
                    val = true;
                    break;
                case 'false':
                    val = false;
                    break;
                case undefined:
                    return;
            }
            if (typeof val === 'object') {
                return;
            }
            this.$slick.slick('slickSetOption', key, val, true);
        },
        
        // It loops parses JSON records and calls _handleRecord on each
        handleRecords: function(records) {
            _.each(JSON.parse(records), $.proxy(this._handleRecord, this)); 
        },
        
        // Accepts a record object and appends to slick
        _handleRecord: function(record) {
            var $img = $('<img>');
            var $div = $('<div class="thumbnail">');
            var $href = $('<a>').attr('href', record[this.uriField]);
            var $title = $('<h5>').text(record[this.fields[0]]);
            var $caption = $('<div class="caption">').append($title);
            $div.append($href);
            var imgUri = this.baseUri + '/' + record.id + '/' + this.imageField;
            $img.attr('data-lazy', imgUri);
            $href.append($img).append($caption);
            this.$slick.append($div);
            this.$slick.slick('slickAdd', $div);
            this.$slick.slick('slickGoTo', 0);
        },
        
        start: function() {
            this.widgetOptions = this.$target.data('options');
            this.$slick = $('<div class="o_slick_container oe_structure">');
            this.$target.html(this.$slick);
            
            if (!this.widgetOptions) {
                this.widgetOptions = defaults;
                this.$target.attr('data-options', JSON.stringify(this.widgetOptions));
            }
            
            this.$slick.slick(this.widgetOptions);
            
            this.$slick.on('set-option', $.proxy(this.slickSetOption, this));
            
            this.model = this.widgetOptions.data_model;
            this.domain = this.widgetOptions.data_domain;
            this.imageField = this.widgetOptions.data_image_field;
            this.dataLimit = this.widgetOptions.data_limit;
            this.nameField = this.widgetOptions.data_name_field;
            this.titleTag = this.widgetOptions.data_title_tag;
            this.titleStr = this.widgetOptions.data_title;
            this.titleClass = this.widgetOptions.data_title_class;
            this.uriField = this.widgetOptions.data_uri_field;
            this.baseUri = '/web/image/' + this.model;
            this.fields = [this.nameField, this.uriField, 'id'];
            var $titleEl = $('<' + this.titleTag + '>');
            $titleEl.text(this.titleStr).addClass(this.titleClass);
            this.$target.prepend($('<div class="row">').append($titleEl));
            this.$target.css('width', this.widgetOptions.data_container_width);
            
            this.getRecords();
            
            return this._super();
          
        },
        
        getRecords: function() {
            // Explicitly encode the data structures to preserve during transfer 
            return $.ajax({
                url: '/website/data_slider/' + this.model,
                method: 'GET',
                data: {
                    domain: JSON.stringify(this.domain),
                    fields: JSON.stringify(this.fields),
                    limit: this.limit,
                },
                success: $.proxy(this.handleRecords, this),
            });
        }
      
    });
  
    return {
        defaults: defaults,
        DataSlider: animation.registry.data_slider,
    };
  
});
