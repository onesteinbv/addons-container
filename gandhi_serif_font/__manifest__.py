# Copyright 2023 Anjeel Haria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Gandhi Serif Font",
    "summary": "Adds Gandhi Serif Font",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Anjeel Haria",
    "depends": ["web"],
    "assets": {
        "web.report_assets_common": [
            "gandhi_serif_font/static/src/scss/fonts.scss",
        ],
        'web._assets_primary_variables': [
            "gandhi_serif_font/static/src/scss/fonts.scss",
            ("prepend", "gandhi_serif_font/static/src/scss/primary_variables.scss"),
        ],
    },
}
