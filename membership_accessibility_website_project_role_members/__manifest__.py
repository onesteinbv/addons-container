# Copyright 2023 Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Membership Accessibility",
    "summary": "Adds options for members to fill in their description and also an option to stay anonymous in the user profile page.",
    "version": "16.0.1.0.0",
    "category": "Membership",
    "author": "Onestein",
    "website": "https://www.onestein.eu",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["membership_accessibility", "website_project_role_members"],
    "data": ["views/views.xml"],
}
