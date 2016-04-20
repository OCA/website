// Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('website_cookie_notice.load_cookiecuttr', function(require) {
  'use strict';
  require('web_editor.base').ready().then(function() {
    $.cookieCuttr();
  });
});
