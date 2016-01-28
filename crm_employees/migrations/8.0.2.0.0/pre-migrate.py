# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp.models import MAGIC_COLUMNS

_logger = logging.getLogger(__name__)

OLD_MODULE = "crm_employees"
NEW_MODULE = "partner_employee_quantity"


def dashed(name):
    return name.replace(".", "_")


def psql_catch(sentence, exception):
    """Catch exceptions in PL/pgSQL.

    :param str sentence:
        Sentence(s) to try. It must end with colon.

    :param str exception:
        Exception to catch.
    """
    return """DO $$
        BEGIN {}
        EXCEPTION WHEN {} THEN RAISE NOTICE '{} caught';
        END $$""".format(sentence, exception, exception.replace("'", "''"))


def model_remove(oldmodel, oldmodule=OLD_MODULE):
    """Remove all occurences of :param:`oldmodel`."""
    sentences = (
        """DELETE FROM ir_model_data
           WHERE module = '{oldmodule}' AND
                 (name = 'model_{oldtable}' OR
                  name LIKE 'field_{oldtable}_%')""",
        """DELETE FROM ir_model_fields
           WHERE model_id = (SELECT id
                             FROM ir_model
                             WHERE model = '{oldmodel}')""",
        "DELETE FROM ir_model WHERE model = '{oldmodel}'",
        "DROP TABLE IF EXISTS {oldtable}",
    )

    for s in sentences:
        yield s.format(
            oldmodel=oldmodel,
            oldtable=dashed(oldmodel),
            oldmodule=oldmodule,
        )


def model_rename(oldmodel, newmodel, transfercols=tuple(),
                 oldmodule=OLD_MODULE, newmodule=NEW_MODULE):
    """Rename a model. Transfer it to :param:`newmodule`.

    If you only want to transfer it from old module to new one, set
    :param:`oldmodel` and :param:`newmodel` the same value.

    :param str oldmodel:
        Old model name, like ``res.partner``.

    :param str newmodel:
        New model name, like ``res.partner``.

    :param iterable transfercols:
        Iterable with names of columns to transfer from :param:`oldmodel` to
        :param:`newmodel`. They will not be renamed.

    :param str oldmodule:
        Old module name, like ``website_blog``.

    :param str newmodule:
        New module name, like ``website_blog``.
    """
    sentences = (
        # Common constraints
        psql_catch(
            "ALTER SEQUENCE {oldtable}_id_seq RENAME TO {newtable}_id_seq;",
            "duplicate_table"),
        psql_catch(
            "ALTER INDEX {oldtable}_pkey RENAME TO {newtable}_pkey;",
            "duplicate_table"),
        psql_catch(
            """ALTER TABLE {oldtable}
               RENAME CONSTRAINT {oldtable}_create_uid_fkey
               TO {newtable}_create_uid_fkey;""",
            "duplicate_object"),
        psql_catch(
            """ALTER TABLE {oldtable}
               RENAME CONSTRAINT {oldtable}_write_uid_fkey
               TO {newtable}_write_uid_fkey;""",
            "duplicate_object"),

        # Rename table in DB
        psql_catch(
            "ALTER TABLE {oldtable} RENAME TO {newtable};",
            "duplicate_table"),

        # Rename model in Odoo, and change owner addon
        "UPDATE ir_model SET model = '{newmodel}' WHERE model = '{oldmodel}'",
        """UPDATE ir_model_data
           SET module = '{newmodule}', name = 'model_{newtable}'
           WHERE module = '{oldmodule}' AND
                 name = 'model_{oldtable}' AND
                 NOT EXISTS (SELECT id
                             FROM ir_model_data
                             WHERE module = '{newmodule}' AND
                                   name = 'model_{newtable}')""",
        """UPDATE ir_model_data
           SET module = '{newmodule}',
               name = REPLACE(name, 'field_{oldtable}', 'field_{newtable}')
           WHERE module = '{oldmodule}' AND
                 name LIKE 'field_{newtable}_%' AND
                 NOT EXISTS (SELECT id
                             FROM ir_model_data
                             WHERE module = '{newmodule}' AND
                                   name = REPLACE(name,
                                                  'field_{oldtable}',
                                                  'field_{newtable}'))""",
    )

    for s in sentences:
        yield s.format(
            oldmodule=oldmodule,
            newmodule=newmodule,
            oldmodel=oldmodel,
            newmodel=newmodel,
            oldtable=dashed(oldmodel),
            newtable=dashed(newmodel),
        )

    for col in transfercols:
        for s in column_rename(newmodel, col, col, oldmodule, newmodule):
            yield s


def column_rename(model, oldcol, newcol,
                  oldmodule=OLD_MODULE, newmodule=NEW_MODULE):
    """Rename a column within a model.

    If you only want to transfer it from old module to new one, set
    :param:`oldcol` and :param:`newcol` the same value.

    :param str model:
        Model name, like ``res.partner``.

    :param str oldcol:
        Old column name, like ``parent_id``.

    :param str newcol:
        New column name, like ``parent_id``.

    :param str oldmodule:
        Old module name, like ``website_blog``.

    :param str newmodule:
        New module name, like ``website_blog``.
    """
    sentences = (
        "ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {table}_{oldcol}_fkey",
        psql_catch(
            "ALTER TABLE {table} RENAME COLUMN {oldcol} TO {newcol};",
            "duplicate_column"),
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

    for s in sentences:
        yield s.format(
            oldcol=oldcol,
            newcol=newcol,
            oldmodule=oldmodule,
            newmodule=newmodule,
            model=model,
            table=dashed(model),
        )


def secure_migration(cr, *args):
    """Run all migration inside a savepoint.

    :param cr:
        DB cursor.

    :param *args:
        Undefined amount of iterables or generators with sentences.
    """
    with cr.savepoint():
        for sentences in args:
            for sentence in sentences:
                _logger.info("Executing:\n%s", sentence)
                cr.execute(sentence)


def migrate(cr, version):
    """Deprecate in favor of OCA's ``partner_employees``."""

    secure_migration(
        cr,
        model_rename("crm.employees_range",
                     "res.partner.employee_quantity_range",
                     MAGIC_COLUMNS + ["name"]),
        model_remove("crm.employees_range"),
        model_rename("res.partner", "res.partner"),
        column_rename("res.partner", "employees_number", "employee_quantity"),
        column_rename("res.partner",
                      "employees_range",
                      "employee_quantity_range_id"),
    )

    _logger.warn(
        "DEPRECATED. Install %s and uninstall %s.",
        NEW_MODULE,
        OLD_MODULE)
