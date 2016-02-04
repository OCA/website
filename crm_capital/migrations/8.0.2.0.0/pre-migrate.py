# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def dashed(name):
    return name.replace(".", "_")


def migrate(cr, version):
    """Deprecate in favor of OCA's ``partner-capital``."""
    oldmodule = "crm_capital"
    newmodule = "partner_capital"

    sentences = (
        """ALTER TABLE crm_turnover_range
           RENAME TO res_partner_turnover_range""",
        """ALTER SEQUENCE crm_turnover_range_id_seq
           RENAME TO res_partner_turnover_range_id_seq""",
        """ALTER INDEX crm_turnover_range_pkey
           RENAME TO res_partner_turnover_range_pkey""",
        """ALTER TABLE res_partner_turnover_range
           RENAME CONSTRAINT crm_turnover_range_create_uid_fkey
           TO res_partner_turnover_range_create_uid_fkey""",
        """ALTER TABLE res_partner_turnover_range
           RENAME CONSTRAINT crm_turnover_range_write_uid_fkey
           TO res_partner_turnover_range_write_uid_fkey""",
        """UPDATE ir_model_data
           SET module = 'partner_capital'
           WHERE module = 'crm_capital' AND
                 name LIKE 'field_res_partner_%'""",
        """UPDATE ir_model_data
           SET name = REPLACE(name,
                              'crm_turnover_range',
                              'res_partner_turnover_range'),
               module = 'partner_capital'
           WHERE module = 'crm_capital' AND
                 name LIKE 'field_crm_turnover_range%'""",
        """UPDATE ir_model
           SET model = 'res.partner.turnover_range'
           WHERE model = 'crm.turnover_range'""",
        """UPDATE ir_translation
           SET name = REPLACE(name,
                              'crm.turnover_range,',
                              'res.partner.turnover_range,')
           WHERE name LIKE 'crm.turnover_range,%' AND
                 (module = '' OR module IS NULL)""",
    )

    renamed_fields = {
        "res.partner": (
            ("capital_country", "capital_country_id"),
            ("capital_registered", "capital_amount"),
            ("turnover_range", "turnover_range_id"),
        )
    }

    with cr.savepoint():
        for sentence in sentences:
            _logger.info("Executing:\n%s", sentence)
            cr.execute(sentence)

        # Column renames
        sentences = (
            """ALTER TABLE {table}
               DROP CONSTRAINT IF EXISTS {table}_{oldcol}_fkey""",
            'ALTER TABLE {table} RENAME COLUMN {oldcol} TO {newcol}',
            """UPDATE ir_model_data
               SET name = 'field_{table}_{newcol}',
                   module = '{newmodule}'
                WHERE module = '{oldmodule}' AND
                      name LIKE 'field_{table}_{oldcol}' AND
                      NOT EXISTS (SELECT id
                                  FROM ir_model_data
                                  WHERE name = 'field_{table}_{newcol}' AND
                                        module = '{newmodule}')""",
            """UPDATE ir_model_data
               SET name = CONCAT('field_{table}_{newcol}', res_id),
                   module = '{newmodule}'
                WHERE module = '{oldmodule}' AND
                      name LIKE 'field_{table}_{oldcol}' AND
                      EXISTS (SELECT id
                              FROM ir_model_data
                              WHERE name = 'field_{table}_{newcol}' AND
                                    module = '{newmodule}')""",
            """UPDATE ir_model_fields
               SET name = '{newcol}'
               WHERE name = '{oldcol}' AND
                     model_id = (SELECT id
                                 FROM ir_model
                                 WHERE model = '{model}')""",
        )
        for model, fields in renamed_fields.iteritems():
            for sentence in sentences:
                for oldcol, newcol in fields:
                    query = sentence.format(
                        model=model,
                        table=dashed(model),
                        oldcol=oldcol,
                        newcol=newcol,
                        oldmodule=oldmodule,
                        newmodule=newmodule,
                    )
                    _logger.info("Executing:\n%s", query)
                    # import wdb; wdb.set_trace()  # TODO DELETE
                    cr.execute(query)

    _logger.warn("DEPRECATED. Install partner_capital and uninstall this.")
