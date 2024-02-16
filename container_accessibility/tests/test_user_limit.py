from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tools import config


class TestUserLimit(TransactionCase):
    def test_exceeded(self):
        # FIXME: Created just to increase code coverage, due to time limitation
        config["user_limit"] = "5"
        with self.assertRaises(UserError):
            for i in range(10):
                self.env["res.users"].create(
                    {
                        "name": "User %s" % i,
                        "login": "User %s" % i,
                        "groups_id": [
                            self.ref("container_accessibility.group_restricted")
                        ],
                    }
                )
        config["user_limit"] = "0"
