/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define_section('website_snippet_barcode', ['module_name.ExportedObject'], function(test) {
    "use strict";

    test('It should demonstrate a PhantomJS test for web (backend)',
        function(assert, ExportedObject) {
            var expect = 'Expected Return',
                result = new ExportedObject();
            assert.assertStrictEqual(
                result,
                expect,
                "Result !== Expect and the test failed with this message"
            );
        }
    );

});
