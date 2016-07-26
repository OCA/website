(function() {
    "use strict";
    var website = openerp.website;

    website.snippet.options["param_entry"]= openerp.website.snippet.Option.extend(
            {   
                select: function (event, np)
                {  
                    var selection = event.$next.first().attr('data-value').split("_");
                    var content = this.$target; 
                    content.attr('data-parameter_id', selection[0])
                        .attr('data-record_id', selection[1]);
                },
                start: function()
                {   
                    this.$target.find('.parametricTemplate').html("click here to select");
                },
                onFocus: function()
                {  
                    this.$target.find('.parametricTemplate').html("Select record to display from options");
                },
                clean_for_save: function() 
                {
                    this.$target.find('.parametricTemplate')
                        .empty()
                        .append(
                                jQuery('<t />')
                                .attr('t-call', 'my_module_name.snippet_content_tmpl')
                                .attr('t-ignore-branding', '1')
                                .append(
                                    jQuery('<t />')
                                    .attr('t-value', this.$target.attr('data-record_id'))
                                    .attr('t-set', 'record_id')
                                    .attr('t-ignore-branding', '1'),
                                    )

                               );
                }
            });
})();
