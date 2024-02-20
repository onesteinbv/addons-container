from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestDedicatedServerCheck(TransactionCase):
    def test_disabled(self):
        """Check if mass mailing still works if mass_mailing_force_dedicated_server.enabled is False"""
        self.env["ir.config_parameter"].set_param(
            "mass_mailing_force_dedicated_server.enabled", False
        )
        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        mailing.action_test()
        mailing.action_put_in_queue()
        mailing.action_schedule()

    def test_enabled_not_configured(self):
        """Check if mass mailing is failing when mass_mailing_force_dedicated_server.enabled is True and dedicated server is not configured"""
        self.env["ir.config_parameter"].set_param(
            "mass_mailing_force_dedicated_server.enabled", True
        )
        self.env["ir.config_parameter"].set_param("mass_mailing.mail_server_id", "0")
        self.env["ir.config_parameter"].set_param(
            "mass_mailing.outgoing_mail_server", "False"
        )

        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        with self.assertRaises(UserError):
            mailing.action_test()
        with self.assertRaises(UserError):
            mailing.action_put_in_queue()
        with self.assertRaises(UserError):
            mailing.action_schedule()

    def test_enabled_configured(self):
        """Check if mass mailing is failing when mass_mailing_force_dedicated_server.enabled is True and dedicated server is configured"""
        mail_server = self.env["ir.mail_server"].create(
            {"name": "mail server", "smtp_host": "localhost"}
        )
        self.env["ir.config_parameter"].set_param(
            "mass_mailing_force_dedicated_server.enabled", True
        )
        self.env["ir.config_parameter"].set_param(
            "mass_mailing.mail_server_id", mail_server.id
        )
        self.env["ir.config_parameter"].set_param(
            "mass_mailing.outgoing_mail_server", "True"
        )

        mailing = self.env["mailing.mailing"].create({"subject": "normal test"})
        mailing.action_test()
        mailing.action_put_in_queue()
        mailing.action_schedule()

        mailing.mail_server_id = False
        with self.assertRaises(UserError):
            mailing.action_test()
        with self.assertRaises(UserError):
            mailing.action_put_in_queue()
        with self.assertRaises(UserError):
            mailing.action_schedule()
