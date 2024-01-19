# Copyright 2017-2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "HR Recruitment labels",
    "summary": "Add's labels on job offers",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Human Resources/Recruitment",
    "version": "16.0.1.0.2",
    "license": "AGPL-3",
    "depends": [
        "hr_recruitment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_job_views.xml",
        "views/hr_job_label_views.xml",
    ],
}
