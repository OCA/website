odoo.define('website.tour.blog.filters', function(require) {
    'use strict';

    var core = require('web.core');
    var Tour = require('web.Tour');
    var base = require('web_editor.base');

    var _t = core._t;

    base.ready().done(function () {

        Tour.register({
            id: 'blog_filters',
            name: _t('Filtering Blog Posts'),
            steps: [
                {
                    title: _t('Filtering and Sorting'),
                    content: _t('Here you can select a filter or sorting option.'),
                    element: 'select[name=blog_posts_selector]',
                    placement: 'bottom',
                },
            ]
        });

    });

});