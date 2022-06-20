def migrate(cr, version):
    # Uses a recursive query:
    # https://www.postgresql.org/docs/current/queries-with.html
    cr.execute(
        """
    WITH RECURSIVE child_views AS (
        SELECT
            id,
            inherit_id,
            name
        FROM
            ir_ui_view
        WHERE
            name ilike 'res_config_settings_view_form_inherit_website'
        UNION
        SELECT
            i.id,
            i.inherit_id,
            i.name
        FROM
            ir_ui_view i
            INNER JOIN child_views c ON c.id = i.inherit_id
    )
    DELETE FROM
        ir_ui_view
    WHERE
        id IN (
            SELECT
                id
            FROM
                child_views
        );
        ;
        """
    )
