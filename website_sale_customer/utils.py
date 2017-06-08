import logging
logger = logging.getLogger(__file__)

try:
    # try to use https://pypi.python.org/pypi/validate_email
    from validate_email import validate_email
except ImportError:
    msg = '"validate_email" package is missing. \
    Install it to have better email validation.'
    logger.warn(msg)

    import re
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def validate_email(email, verify=False, check_mx=False):
        """ fallback validation.
        `verify` and `check_mx``are just to mimic
        `validate_email.validate_email` signature.
        """
        return EMAIL_REGEX.match(email)

try:
    # improves `validate_email.validate_email` validation
    # see https://pypi.python.org/pypi/validate_email docs
    import DNS # noqa
    HAS_PyDNS = True
except ImportError:
    msg = '"pyDNS" package is missing. \
    Install it to have better email validation.'
    logger.warn(msg)
    HAS_PyDNS = False

try:
    import phonenumbers
    from phonenumbers.phonenumberutil import NumberParseException

    def validate_phonenumber(value):
        try:
            return bool(phonenumbers.parse(value))
        except NumberParseException:
            return False

except ImportError:
    msg = '"phonenumbers" package is missing. \
    Install it to have better email validation.'
    logger.warn(msg)

    def validate_phonenumber(value):
        if not value.isdigit():
            return False
        return True
