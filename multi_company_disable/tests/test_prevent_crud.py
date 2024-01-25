from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestPreventCrud(TransactionCase):
    def test_creation(self):
        with self.assertRaises(AccessError):
            with self.with_user("admin"):
                self.env["res.company"].create({"name": "My company"})
        self.env["res.company"].create({"name": "My company 2"})
