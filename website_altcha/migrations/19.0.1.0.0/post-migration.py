def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        UPDATE website
           SET altcha_algorithm = CASE altcha_algorithm
                   WHEN 'SHA256' THEN 'SHA-256'
                   WHEN 'SHA384' THEN 'SHA-384'
                   WHEN 'SHA512' THEN 'SHA-512'
               END
         WHERE altcha_algorithm IN ('SHA256', 'SHA384', 'SHA512')
        """
    )
