/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('website_portal_contact.tour', function (require) {
  'use strict'

  var tour = require('web_tour.tour')
  var core = require('web.core')
  var base = require('web_editor.base')
  var steps = [{
    content: 'Click to add Guybrush',
    trigger: 'div.col-md-4.col-md-offset-4.mt8 > a',
    waitFor: 'div.col-md-4.col-md-offset-4.mt8 > a',
    position: 'top',
    run: 'click'
  },
  {
    content: 'Fill name "Guybrush Threpwood"',
    trigger: '#name',
    run: 'text Guybrush Threpwood'
  },
  {
    content: 'Fill phone',
    trigger: '#phone',
    run: 'text 987654321'
  },
  {
    content: 'Fill mobile',
    trigger: '#mobile',
    run: 'text 123456789'
  },
  {
    content: 'Fill email "guybrush@example.com"',
    trigger: '#email',
    run: 'text guybrush@example.com'
  },
  {
    content: 'Save new contact Guybrush',
    trigger: '#portal_contact > section > div > button',
    run: 'click',
    wait: 11500
  },
  {
    content: 'Return to list',
    trigger: 'a[href="/my/contacts"]',
    run: 'click'
  },
  {
    content: 'Search for Guybrush',
    trigger: '#wrap > div > div.col-md-8 > div.row.mt16.mb16 > div:nth-child(1) > form > div > input',
    waitFor: '#wrap > div > div.col-md-8 > div.row.mt16.mb16 > div:nth-child(1) > form > div > input',
    position: 'top',
    run: 'text guybrush'
  },
  {
    content: 'Click search for Guybrush',
    position: 'top',
    trigger: '#wrap > div > div.col-md-8 > div.row.mt16.mb16 > div:nth-child(1) > form > div > span > button',
    run: 'click'
  },
  {
    content: 'Delete Guybrush',
    trigger: 'tr:contains("Guybrush") td.text-center > a',
    waitFor: 'tr:contains("Guybrush")',
    run: 'click'
  },
  {
    content: 'Return to list',
    trigger: 'a[href="/my/contacts"]',
    run: 'click'
  }
  ]

  tour.register('website_portal_contact_tour',
    {url: '/my/contacts',
      wait_for: base.ready(),
      'skip_enabled': true},
    steps)
})
