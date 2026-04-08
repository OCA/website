from . import controllers
from . import models
import uuid


def post_init_hook(env):
    """Ensure that the altcha.key parameter exists in the ir_config_parameter table."""
    param_obj = env["ir.config_parameter"].sudo()
    if not param_obj.get_param("altcha.key"):
        param_obj.set_param("altcha.key", str(uuid.uuid1()))
