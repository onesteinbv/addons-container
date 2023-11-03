from odoo import _, http
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.addons.web.controllers.home import Home


class HomeController(Home):

    @http.route()
    def switch_to_admin(self):
        if request.env.user.is_restricted_user():
            raise AccessError(_("Access Denied"))
        return super().switch_to_admin()
