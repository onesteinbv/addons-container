# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Accounting Consolidation",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Onestein BV, André Schenkels",
    "website": "https://www.onestein.eu",
    "category": "Accounting",
    "summary": "",
    "depends": ["account"],
    "excludes": ["account_consolidation"],
    "data": [
        "security/ir.model.access.csv",
        # "views/assets_backend.xml",
        "views/account_account_views.xml",
        "views/consolidation_account_views.xml",
        "views/consolidation_chart_views.xml",
        "views/consolidation_group_views.xml",
        "views/account_move_views.xml",
        "views/menu.xml",
    ],
    # "qweb": ["static/src/xml/account_reconciliation.xml"],
    "installable": True,
}
