from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "res.config.settings",
                "res_config_settings",
                "has_piwik_analytics",
                "has_matomo_analytics",
            ),
            (
                "res.config.settings",
                "res_config_settings",
                "piwik_analytics_id",
                "matomo_analytics_id",
            ),
            (
                "res.config.settings",
                "res_config_settings",
                "piwik_analytics_host",
                "matomo_analytics_host",
            ),
            (
                "website",
                "website",
                "has_piwik_analytics",
                "has_matomo_analytics",
            ),
            (
                "website",
                "website",
                "piwik_analytics_id",
                "matomo_analytics_id",
            ),
            (
                "website",
                "website",
                "piwik_analytics_host",
                "matomo_analytics_host",
            ),
        ],
    )
