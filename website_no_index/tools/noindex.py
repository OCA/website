import re
import logging
import fnmatch

from odoo.http import request

_logger = logging.getLogger(__name__)
regex = re.compile(r'<[^>]*>')


def parse_noindex_param(endpoint):
    noindex = endpoint.routing.get('noindex', [])
    return noindex


def should_set_in_header():
    return request.endpoint is not None \
        and 'header' in parse_noindex_param(request.endpoint)


def should_set_in_meta():
    return request.endpoint is not None \
        and 'meta' in parse_noindex_param(request.endpoint)


def should_set_in_robots(endpoint):
    return 'robots' in parse_noindex_param(endpoint)


def create_routes_tree(rules):
    """
    Use the werkzeug rules to generate a route tree. With the noindex
    indications.
    """
    root = RouteNode()

    for rule in rules:
        route = rule.rule
        route = regex.sub('*', route)
        noindex = should_set_in_robots(rule.endpoint)
        root.add_endpoint(route.lstrip('/'), noindex=noindex)

    return root


class RouteNode:
    def __init__(self, parent=None, section=None):
        self.children = {}
        self.noindex = False
        self.is_endpoint = False
        self.parent = parent
        self.section = section or ""

    def add_endpoint(self, route, noindex=False):
        """
        Add an endpoint route to the tree. If they don't exists, create the
        intermediary nodes.
        :param route: The route path without a starting slash.
        :param noindex: Indicate if the endpoint should be indexed.
        :return: The node corresponding to the endpoint.
        """
        sections = route.split('/', 1)
        if sections[0]:
            child_route = sections[1] if len(sections) > 1 else ""
            child = self.children.setdefault(sections[0],
                                             RouteNode(parent=self,
                                                       section=sections[0]))
            return child.add_endpoint(child_route, noindex=noindex)
        else:
            if self.is_endpoint:
                path = self.get_path()
                _logger.warning(f"Endpoint {path} already exists")
            self.is_endpoint = True
            self.noindex = noindex
        return self

    def get_path(self):
        path = self.parent._get_path() if self.parent else "/"
        path += f"{self.section}"
        return path

    def _get_path(self):
        """
        Return the path to access the current RouteNode.
        """
        path = self.parent._get_path() if self.parent else ""
        path += f"{self.section}/"
        return path

    def get_robots(self):
        """
        Return a list of access rules for robots.txt. With these rules, the
        legitimate robots that crawl the website know which endpoints shouldn't
        be explored.

        The list is the most simplified it can be (assuming that allow is the
        default access rule).
        """
        robots = []
        if self.is_endpoint and self.noindex:
            robots.append('Disallow: /')
        robots.extend(self._get_robots('/', branch_noindexed=self.noindex))
        return robots

    def _get_robots(self, path, branch_noindexed=False):
        """
        Used by get_robots() to walk the route tree.
        :param path: The current path to this node.
        :param branch_noindexed: Indicates whether the current Route branch
            allows the crawling of robots.
        :return: The list of access rules.
        """
        robots = []
        wildcard_endpoints = {}

        # Wildcard sections
        wildcards = {k: v for k, v in self.children.items() if '*' in k}
        for section, node in wildcards.items():
            route = "{path}{section}"
            branch = branch_noindexed
            if node.is_endpoint:
                access = ""
                if branch and not node.noindex:
                    access = "Allow:    %s"
                    branch = False
                elif not branch and node.noindex:
                    access = "Disallow: %s"
                    branch = True
                if access:
                    robots.append(access % route)
                    wildcard_endpoints[section] = node

            robots.extend(node._get_robots(route + "/",
                                           branch_noindexed=branch))

        # Other sections
        children = {k: v for k, v in self.children.items() if '*' not in k}
        for section, node in children.items():
            route = "{path}{section}"
            branch = branch_noindexed
            if node.is_endpoint:
                access = ""

                # Check if one of the wildcards has an effect on the current
                # section.
                wild_node = None
                for wild, n in wildcard_endpoints.items():
                    if fnmatch.fnmatch(section, wild):
                        wild_node = n
                        break
                if wild_node:
                    branch = wild_node.noindex

                if branch and not node.noindex:
                    access = "Allow:    %s"
                    branch = False
                elif not branch and node.noindex:
                    access = "Disallow: %s"
                    branch = True
                if access:
                    robots.append(access % route)
            robots.extend(node._get_robots(route + "/",
                                           branch_noindexed=branch))

        return robots
