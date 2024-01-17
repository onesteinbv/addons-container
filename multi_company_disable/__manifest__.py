{
    "name": "Disable Multi-company",
    "summary": "Remove multi-company features for all users",
    "category": "Technical",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base", "web"],
    "data": ["views/res_company_view.xml", "views/res_users_view.xml"],
    "assets": {
        "web.assets_backend": ["multi_company_disable/static/src/js/backend.esm.js"]
    },
}
