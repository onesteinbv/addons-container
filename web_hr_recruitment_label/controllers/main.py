# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools
import logging

from odoo import _, http
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

_logger = logging.getLogger(__name__)


def job_routes():
    prefix = "/jobs"
    filters = [
        '/country/<model("res.country"):country>',
        '/department/<model("hr.department"):department>',
        "/office/<int:office_id>",
        "/employment_type/<int:contract_type_id>",
        "/label/<int:label_id>",
    ]
    routes = ["/jobs"]
    for L in range(len(filters) + 1):
        for subset in itertools.combinations(filters, L):
            routes.append(prefix + "".join(subset))
    return routes


class WebsiteHrRecruitment(WebsiteHrRecruitment):
    def sitemap_jobs(self, rule, qs):
        if not qs or qs.lower() in "/jobs":
            yield {"loc": "/jobs"}

    @http.route(
        job_routes(), type="http", auth="public", website=True, sitemap=sitemap_jobs
    )
    def jobs(
        self,
        country=None,
        department=None,
        office_id=None,
        contract_type_id=None,
        label_id=None,
        **kwargs,
    ):
        renv = request.env(
            context=dict(request.env.context, show_address=True, no_tag_br=True)
        )

        Country = renv["res.country"]
        Jobs = renv["hr.job"]

        # List jobs available to current UID
        domain = request.website.website_domain()
        job_ids = Jobs.search(
            domain, order="is_published desc, sequence, no_of_recruitment desc"
        ).ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)

        # Default search by user country
        if not (
            country
            or department
            or office_id
            or contract_type_id
            or kwargs.get("all_countries")
        ):
            country_code = request.geoip.get("country_code")
            if country_code:
                countries_ = Country.search([("code", "=", country_code)])
                country = countries_[0] if countries_ else None
                if not any(
                    j
                    for j in jobs
                    if j.address_id and j.address_id.country_id == country
                ):
                    country = False

        # Filter job / office for country
        if country and not kwargs.get("all_countries"):
            jobs = [
                j
                for j in jobs
                if not j.address_id or j.address_id.country_id.id == country.id
            ]
            offices = {
                j.address_id
                for j in jobs
                if not j.address_id or j.address_id.country_id.id == country.id
            }
        else:
            offices = {j.address_id for j in jobs if j.address_id}

        # Deduce departments and countries offices of those jobs
        departments = {j.department_id for j in jobs if j.department_id}
        countries = {o.country_id for o in offices if o.country_id}
        employment_types = {j.contract_type_id for j in jobs if j.contract_type_id}
        labels = renv["hr.job.label"]
        for j in jobs:
            labels = labels | j.label_ids
        labels.sorted(lambda r: r.id)
        labels = set(labels)

        if department:
            jobs = [
                j
                for j in jobs
                if j.department_id and j.department_id.id == department.id
            ]
        if office_id and office_id in [x.id for x in offices]:
            jobs = [j for j in jobs if j.address_id and j.address_id.id == office_id]
        else:
            office_id = False
        if contract_type_id:
            jobs = [
                j
                for j in jobs
                if j.contract_type_id and j.contract_type_id.id == contract_type_id
            ]
        if label_id:
            jobs = [j for j in jobs if j.label_ids and label_id in j.label_ids.ids]

        _logger.info(labels)
        _logger.info(label_id)
        _logger.info(kwargs)
        # Render page
        return request.render(
            "website_hr_recruitment.index",
            {
                "jobs": jobs,
                "countries": countries,
                "departments": departments,
                "offices": offices,
                "employment_types": employment_types,
                "labels": labels,
                "country_id": country,
                "department_id": department,
                "office_id": office_id,
                "contract_type_id": contract_type_id,
                "label_id": label_id,
            },
        )

    @http.route("/jobs/add", type="json", auth="user", website=True)
    def jobs_add(self, **kwargs):
        # avoid branding of website_description by setting rendering_bundle in context
        job = (
            request.env["hr.job"]
            .with_context(rendering_bundle=True)
            .create(
                {
                    "name": _("Job Title"),
                }
            )
        )
        return f"/jobs/detail/{slug(job)}"

    @http.route(
        """/jobs/detail/<model("hr.job"):job>""",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def jobs_detail(self, job, **kwargs):
        return request.render(
            "website_hr_recruitment.detail",
            {
                "job": job,
                "main_object": job,
            },
        )

    @http.route(
        """/jobs/apply/<model("hr.job"):job>""",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def jobs_apply(self, job, **kwargs):
        error = {}
        default = {}
        if "website_hr_recruitment_error" in request.session:
            error = request.session.pop("website_hr_recruitment_error")
            default = request.session.pop("website_hr_recruitment_default")
        return request.render(
            "website_hr_recruitment.apply",
            {
                "job": job,
                "error": error,
                "default": default,
            },
        )
