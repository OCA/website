def migrate(cr, version):
    cr.execute(
        """
        update ir_ui_view set active='f' where name ilike
        'res_config_settings_view_form_inherit_website'
        """
    )
