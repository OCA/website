odoo.define('website_support.color_tree', function (require) {
"use strict";

    var get_eval_context = function(record){
        return _.extend(
            {},
            record.attributes,
            pyeval.context()
        );
    };

    var ListView = require('web.ListView'),
        pyeval = require('web.pyeval'),
        py = window.py;

    ListView.include({

        style_for: function (record)
        {
            var result = this._super.apply(this, arguments);

            if ( 'ticket_color' in record.attributes ) {
                var color = py.evaluate( py.parse( py.tokenize('ticket_color') ), get_eval_context(record) ).toJSON();
			    result += 'color: ' + color + ";";
            }

            return result;
        },
    });


});