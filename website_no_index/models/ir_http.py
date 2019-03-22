# -*- coding: utf-8 -*-
import logging

from ..tools import noindex

from odoo import models

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        """
        Set the X-Robots-Tag header if the endpoint has the corresponding
        noindex parameter.
        """
        response = super(IrHttp, cls)._dispatch()
        if isinstance(response, Exception):
            return response

        if noindex.should_set_in_header():
            response.headers.setdefault('X-Robots-Tag', 'noindex')

        return response

    @classmethod
    def get_endpoint_tree(cls):
        """
        Get or generate the endpoint tree from the existing controllers' routes
        """
        if not hasattr(cls, '_endpoint_tree'):
            cls._generate_endpoint_tree()
        return cls._endpoint_tree

    @classmethod
    def _generate_endpoint_tree(cls):
        """Generate the endpoint tree from the controllers' routes"""
        _logger.info("Generating endpoints tree")
        routing_map = cls.routing_map()
        cls._endpoint_tree = noindex.create_routes_tree(routing_map._rules)
