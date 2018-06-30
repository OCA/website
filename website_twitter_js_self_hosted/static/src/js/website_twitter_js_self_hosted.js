(function() {
    "use strict";
    var website = openerp.website;

    website.snippet.options["jstweetfeed"] = openerp.website.snippet.Option.extend(
    {   
        select: function (event, np)
        {   
            var selection = event.$next.first().attr('data-value').split("_");
            var content = this.$target;  
            content.attr('data-tweettheme_id', selection[1]);
            content.attr('data-tweetfeed_id', selection[0]);
        },
        start: function()
        {   
            this.$target.find('.parametricTemplate').html("click here to select twitter feed");
        },
        onFocus: function()
        {  
            this.$target.find('.parametricTemplate').html("Select twitter feed");
        },
        clean_for_save: function() 
        {
            this.$target.find('.parametricTemplate')
                .empty()
                .append(
                    jQuery('<t />')
                        .attr('t-call', 'website_twitter_js_self_hosted.twitter_feed_content')
                        .attr('t-ignore-branding', '1')
                        .append(
                            jQuery('<t />')
                               .attr('t-value', this.$target.attr('data-tweetfeed_id'))
                               .attr('t-set', 'tweetfeed_id')
                               .attr('t-ignore-branding', '1')
                             )    
                        .append(
                            jQuery('<t />')
                               .attr('t-value', this.$target.attr('data-tweettheme_id'))
                               .attr('t-set', 'tweettheme_id')
                               .attr('t-ignore-branding', '1')
                             )     
                );
        }
    });

})();

