/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('website_portal_contact.tour_portal_contacts', function (require) {
    'use strict';
    
    var core = require('web.core');
    var tour = require("web_tour.tour");
    var _t = core._t;

    tour.register('portal_contacts', {
        url: '/my/contacts',
        sequence: 11,
    },
        [
            {
                content: _t('Check My Contacts Portal Page'),
                trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                extra_trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                in_modal: false,
                position: 'bottom',
                run: function (){} //check My Contacts Portal Page
            },
            {
                content: _t('Cilck on Add new contact button'),
                trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                extra_trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                position: 'bottom',
            },
            {
                content: _t('Click on Name'),
                trigger: ".card-body > #portal_contact #name",
                extra_trigger: ".card-body > #portal_contact #name",
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Fill name'),
                trigger: '.card-body > #portal_contact #name',
                extra_trigger: '.card-body > #portal_contact #name',
                run: 'text Guybrush Threpwood',
                position: 'bottom',
            },
            {
                content: _t('Click on phone'),
                trigger: ".card-body > #portal_contact #phone",
                extra_trigger: ".card-body > #portal_contact #phone",
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Fill phone'),
                trigger: '.card-body > #portal_contact #phone',
                extra_trigger: '.card-body > #portal_contact #phone',
                run: 'text 987654321',
                position: 'bottom',
            },
            {
                content: _t('Click on mobile'),
                trigger: ".card-body > #portal_contact #mobile",
                extra_trigger: ".card-body > #portal_contact #mobile",
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Fill mobile'),
                trigger: '.card-body > #portal_contact #mobile',
                extra_trigger: '.card-body > #portal_contact #mobile',
                run: 'text 123456789',
                position: 'bottom',
            },
            {
                content: _t('Click on email'),
                trigger: ".card-body > #portal_contact #email",
                extra_trigger: ".card-body > #portal_contact #email",
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Fill email'),
                trigger: '.card-body > #portal_contact #email',
                extra_trigger: '.card-body > #portal_contact #email',
                run: 'text guybrush@example.com',
                position: 'bottom',
            },
            {
                content: _t('Save new contact'),
                trigger: '.card-body > #portal_contact .btn:contains("Save")',
                run: 'click',
                position: 'bottom',
            },
            {
                title: _t('Change to Elaine'),
                trigger: '#name',
                extra_trigger: '#name[value="Guybrush Threpwood"]',
                run: 'text Elaine Marley',
                position: 'bottom',
            },
            {
                title: _t('Change Email'),
                trigger: '#email',
                run: 'text elaine@example.com',
                position: 'bottom',
            },
            {
                content: _t('Save changes'),
                trigger: '.card-body > #portal_contact .btn:contains("Save")',
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Delete Elaine'),
                trigger: '.card > .card-header .fa-trash',
                extra_trigger: '#name[value="Elaine Marley"]',
                position: 'bottom',
            },
            {
                content: _t('Click to add LeChuck'),
                trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                extra_trigger: '#wrap .mr-2 > .btn > span:contains("Add new contact")',
                position: 'bottom',
            },
            {
                content: _t('Click on Name'),
                trigger: ".card-body > #portal_contact #name",
                extra_trigger: ".card-body > #portal_contact #name",
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Fill name LeChuck'),
                trigger: '.card-body > #portal_contact #name',
                extra_trigger: '.card-body > #portal_contact #name',
                run: 'text LeChuck',
                position: 'bottom',
            },
            {
                content: _t('Save changes'),
                trigger: '.card-body > #portal_contact .btn:contains("Save")',
                run: 'click',
                position: 'bottom',
            },
            {
                content: _t('Return to list'),
                trigger: '.row .breadcrumb-item:nth-child(2) > a',
                position: 'bottom',
            },
            {
                content: _t('Check Total'),
                trigger: '#wrapwrap .c_total span:contains("1")',
                trigger: '#wrapwrap .c_total span:contains("1")',
                in_modal: false,
                position: 'bottom',
                run: function (){}
            },
            {
                content: _t('Search for Guybrush'),
                trigger: 'input[name=search]',
                extra_trigger: 'input[name=search]',
                run: 'text guybrush',
            },
            {
                content: _t('Click search for Guybrush'),
                trigger: '#o_portal_navbar_content .input-group-append > .btn',
                position: 'bottom',
            },
            {
                content: _t('Check Total'),
                trigger: '#wrapwrap .c_total span:contains("0")',
                trigger: '#wrapwrap .c_total span:contains("0")',
                in_modal: false,
                position: 'bottom',
                run: function (){}
            },
            {
                content: _t('Guybrush not found, search for LeChuck'),
                trigger: 'input[name=search]',
                extra_trigger: 'input[name=search]',
                run: 'text lechuck',
            },
            {
                content: _t('Click search for LeChuck'),
                trigger: '#o_portal_navbar_content .input-group-append > .btn',
                position: 'bottom',
            },
            {
                content: _t('Check Total'),
                trigger: '#wrapwrap .c_total span:contains("1")',
                trigger: '#wrapwrap .c_total span:contains("1")',
                in_modal: false,
                position: 'bottom',
                run: function (){}
            }
    ]);
});