# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    '''Sets the flag for existing installations having an ID set'''
    cr.execute('''
    UPDATE website
        SET has_piwik_analytics=true
        WHERE piwik_analytics_id IS NOT NULL
    ''')
