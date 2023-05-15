# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import werkzeug

from odoo import http
from odoo.http import request
from odoo.tools.translate import _

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_crm_partner_assign.controllers.main import (
    WebsiteCrmPartnerAssign,
)


class WebsiteCrmPartnerAssignCity(WebsiteCrmPartnerAssign):
    def sitemap_partners(self, rule, qs):
        if not qs or qs.lower() in "/partners":
            yield {"loc": "/partners"}

        Grade = self["res.partner.grade"]
        dom = [("website_published", "=", True)]
        dom += sitemap_qs2dom(qs=qs, route="/partners/grade/", field=Grade._rec_name)
        for grade in self["res.partner.grade"].search(dom):
            loc = "/partners/grade/%s" % slug(grade)
            if not qs or qs.lower() in loc:
                yield {"loc": loc}

        partners_dom = [
            ("is_company", "=", True),
            ("grade_id", "!=", False),
            ("website_published", "=", True),
            ("grade_id.website_published", "=", True),
            ("country_id", "!=", False),
        ]
        dom += sitemap_qs2dom(qs=qs, route="/partners/country/")
        countries = (
            self["res.partner"]
            .sudo()
            .read_group(partners_dom, fields=["id", "country_id"], groupby="country_id")
        )
        for country in countries:
            loc = "/partners/country/%s" % slug(country["country_id"])
            if not qs or qs.lower() in loc:
                yield {"loc": loc}

    @http.route(
        [
            # Routes for state
            # URL partners/grade
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/state/<model("res.country.state"):state>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/state/<model("res.country.state"):state>/page/<int:page>',
            # URL partners/state
            '/partners/state/<model("res.country.state"):state>',
            '/partners/state/<model("res.country.state"):state>/page/<int:page>',
            # URL partners/country/state
            '/partners/country/<model("res.country"):country>'
            '/state/<model("res.country.state"):state>',
            '/partners/country/<model("res.country"):country>'
            '/state/<model("res.country.state"):state>/page/<int:page>',
            # URL partners/grade/country/state
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>/state/<model("res.country.state"):state>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>'
            '/state/<model("res.country.state"):state>/page/<int:page>',
            # Routes for city
            # URL partners/city
            '/partners/city/<model("res.city"):city>',
            '/partners/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/country/city
            '/partners/country/<model("res.country"):country>/city/<model("res.partner"):city>',
            '/partners/country/<model("res.country"):country>'
            '/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/state/city
            '/partners/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>',
            '/partners/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/grade/country/state/city
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/grade/state/city
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/state/<model("res.country.state"):state>'
            '/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/grade/country/city
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>'
            '/city/<model("res.city"):city>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/country/<model("res.country"):country>'
            '/city/<model("res.city"):city>/page/<int:page>',
            # URL partners/grade/city
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/city/<model("res.city"):city>',
            '/partners/grade/<model("res.partner.grade"):grade>'
            '/city/<model("res.city"):city>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_partners,
    )
    def partners_by_state_and_city(
        self, country=None, grade=None, state=None, city=None, page=0, **post
    ):
        partner_default = super().partners(
            country=country, grade=grade, state=state, city=city, page=page, **post
        )

        country_all = post.pop("country_all", False)
        partner_obj = request.env["res.partner"]
        country_obj = request.env["res.country"]
        search = post.get("search", "")

        base_partner_domain = [
            ("is_company", "=", True),
            ("grade_id", "!=", False),
            ("website_published", "=", True),
        ]
        if not request.env["res.users"].has_group("website.group_website_publisher"):
            base_partner_domain += [("grade_id.website_published", "=", True)]
        if search:
            base_partner_domain += [
                "|",
                ("name", "ilike", search),
                ("website_description", "ilike", search),
            ]

        # current search

        search_condition = {
            "grade_id": grade.id if grade else False,
            "country_id": country.id if country else False,
            "state_id": state.id if state else False,
            "city_id": city.id if city else False,
        }
        base_partner_domain += [
            (paramater, "=", value)
            for paramater, value in search_condition.items()
            if value
        ]

        # format pager
        url = (
            (
                "/partners/grade/"
                + slug(grade)
                + ("/country/" + slug(country) if country else "")
                + ("/state/" + slug(state) if state else "")
                + ("/city/" + slug(city) if city else "")
            )
            if grade
            else (
                "/partners/country/"
                + slug(country)
                + ("/state/" + slug(state) if state else "")
                + ("/city/" + slug(city) if city else "")
            )
            if country
            else (
                "/partners/state/"
                + slug(state)
                + ("/city/" + slug(city) if city else "")
            )
            if state
            else ("/partners/city/" + slug(city) if city else "/partners")
        )

        url_args = {}
        if search:
            url_args["search"] = search
        if country_all:
            url_args["country_all"] = True

        # group by grade
        grade_domain = list(base_partner_domain)
        country_code = (
            request.session["geoip"].get("country_code")
            if not country and not country_all
            else None
        )
        country = (
            country_obj.search([("code", "=", country_code)], limit=1)
            if country_code
            else None
        )
        grade_domain += [("country_id", "=", country.id)] if country else []
        grade_domain += [("state_id", "=", state.id)] if state else []
        grade_domain += [("city_id", "=", city.id)] if city else []
        # get grades
        grades = partner_obj.sudo().read_group(
            grade_domain, ["id", "grade_id"], groupby="grade_id"
        )
        # count partners in grade
        grades_partners = partner_obj.sudo().search_count(grade_domain)
        # add active grade flag to each grade dict
        for grade_dict in grades:
            grade_dict["active"] = grade and grade_dict["grade_id"][0] == grade.id
        # add "All Grades" option at the beginning of the list
        grades.insert(
            0,
            {
                "grade_id_count": grades_partners,
                "grade_id": (0, _("All Categories")),
                "active": bool(grade is None),
            },
        )

        # group by country
        country_domain = list(base_partner_domain)
        country_domain += [("grade_id", "=", grade.id)] if grade else []
        country_domain += [("state_id", "=", state.id)] if state else []
        country_domain += [("city_id", "=", city.id)] if city else []
        # get countries
        countries = partner_obj.sudo().read_group(
            country_domain,
            ["id", "country_id"],
            groupby="country_id",
            orderby="country_id",
        )
        # count partners in countries
        countries_partners = partner_obj.sudo().search_count(country_domain)
        # add active country flag to each country dict
        for country_dict in countries:
            country_dict["active"] = (
                country
                and country_dict["country_id"]
                and country_dict["country_id"][0] == country.id
            )
        # add "All Countries" option at the beginning of the list
        countries.insert(
            0,
            {
                "country_id_count": countries_partners,
                "country_id": (0, _("All Countries")),
                "active": bool(country is None),
            },
        )

        # group by state
        states_domain = list(base_partner_domain)
        states_domain += [("grade_id", "=", grade.id)] if grade else []
        states_domain += [("country_id", "=", country.id)] if country else []
        states_domain += [("city_id", "=", city.id)] if city else []
        # get states
        states = partner_obj.sudo().read_group(
            states_domain, ["id", "state_id"], groupby="state_id", orderby="state_id"
        )
        # count partners in states
        states_partners = partner_obj.sudo().search_count(states_domain)
        # add active state flag to each state dict
        for state_dict in states:
            state_dict["active"] = (
                state
                and state_dict["state_id"]
                and state_dict["state_id"][0] == state.id
            )
        # add "All States" option at the beginning of the list
        states.insert(
            0,
            {
                "state_id_count": states_partners,
                "state_id": (0, _("All States")),
                "active": bool(state is None),
            },
        )

        # group by city
        cities_domain = list(base_partner_domain)
        cities_domain += [("grade_id", "=", grade.id)] if grade else []
        cities_domain += [("country_id", "=", country.id)] if country else []
        cities_domain += [("state_id", "=", state.id)] if state else []
        # get cities
        cities = partner_obj.sudo().read_group(
            cities_domain, ["id", "city_id"], groupby="city_id", orderby="city_id"
        )
        # count partners in cities
        cities_partners = partner_obj.sudo().search_count(cities_domain)
        # add active state flag to each city dict
        for city_dict in cities:
            city_dict["active"] = (
                city and city_dict["city_id"] and city_dict["city_id"][0] == city.id
            )
        # add "All Cities" option at the beginning of the list
        cities.insert(
            0,
            {
                "city_id_count": cities_partners,
                "city_id": (0, _("All Cities")),
                "active": bool(city is None),
            },
        )

        # count the number of partners that match the search criteria
        partner_count = partner_obj.sudo().search_count(base_partner_domain)
        # set up the pager for the results
        pager = request.website.pager(
            url=url,
            total=partner_count,
            page=page,
            step=self._references_per_page,
            scope=7,
            url_args=url_args,
        )
        # search for partners that match the search criteria, and sort them in a specific order
        partner_ids = partner_obj.sudo().search(
            base_partner_domain,
            order="grade_sequence ASC, implemented_count DESC, display_name ASC, id ASC",
            offset=pager["offset"],
            limit=self._references_per_page,
        )
        partners = partner_ids.sudo()
        # create a comma-separated string of partner IDs for use with the Google Maps API
        google_map_partner_ids = ",".join(str(p.id) for p in partners)
        # get the Google Maps API key from the website configuration
        google_maps_api_key = request.website.google_maps_api_key

        values = {
            # List of countries for filtering partners
            "countries": countries,
            # Flag to indicate if all countries are selected
            "country_all": country_all,
            # Currently selected country
            "current_country": country,
            # List of partner grades for filtering
            "grades": grades,
            # Currently selected partner grade
            "current_grade": grade,
            # Search parameters entered by the user
            "searches": post,
            # Encoded URL query string
            "search_path": "%s" % werkzeug.urls.url_encode(post),
            # List of partners matching search criteria
            "partners": partners,
            # Pager object for pagination
            "pager": pager,
            # Currently selected state
            "current_state": state,
            # List of states for filtering
            "states": states,
            # Currently selected city
            "current_city": city,
            # List of cities for filtering
            "cities": cities,
            # Comma-separated IDs of partners for Google Maps
            "google_map_partner_ids": google_map_partner_ids,
            # API key for Google Maps
            "google_maps_api_key": google_maps_api_key,
        }

        # Update the query context with the values
        partner_default.qcontext.update(values)

        # Return the updated partner_default
        return partner_default

    @http.route()
    def partners(self, country=None, grade=None, state=None, city=None, page=0, **post):
        return self.partners_by_state_and_city(
            country=country, grade=grade, state=state, city=city, page=page, **post
        )
