# Copyright 2023 Onestein- Anjeel Haria
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Website Device Visibility",
    "summary": "Allows to manage visibility of website elements on mobile and desktops",
    "version": "15.0.1.0.0",
    "category": "Website",
    "author": "Onestein",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website"],
    "data": ["views/snippets.xml"],
    "assets": {
        'website.assets_wysiwyg': [
            'website_device_visibility/static/src/js/options.js',
            'website_device_visibility/static/src/js/editor.js',
            'website_device_visibility/static/src/scss/website_device_visibility.scss',
        ],
        'website.website_configurator_assets_scss': [
            'website_device_visibility/static/src/scss/website_device_visibility.scss',
        ],
    },
    "sequence": 1,
}
