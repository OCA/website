from odoo.tests import SavepointCase

ONE_PIXEL = (
    "iVBORw0KGgoAAAANSUhEUgAAAAYAAAAGCAYAAADgzO9IAAAAJElEQVQI"
    "mWP4/b/qPzbM8Pt/1X8GBgaEAJTNgFcHXqOQMV4dAMmObXXo1/BqAAAA"
    "AElFTkSuQmCC"
)


class TestMisc(SavepointCase):
    def test_bin_size(self):
        record = self.env.ref("base.main_partner")
        field_name = "image_1920"

        record.write({field_name: ONE_PIXEL})
        record.invalidate_cache()

        self.env["ir.qweb.field.image"].record_to_html(
            record.with_context(bin_size=True), field_name, {"tagName": "div"}
        )
