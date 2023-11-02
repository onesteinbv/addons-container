from odoo import _, api, fields, models


class OnboardingWizard(models.TransientModel):
    _name = 'base.onboarding.wizard'
    _inherit = ['multi.step.wizard.mixin']
    _description = "Onboarding Wizard"

    def _default_website(self):
        website = self.env['website'].search([('company_id', '=', self.env.company.id)], limit=1)
        if not website:   # Get the first available website if there's no website found for the current active company
            website = self.env['website'].search([], limit=1)
        return website

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company
    )

    website_id = fields.Many2one(
        comodel_name='website',
        default=_default_website
    )

    company_logo = fields.Binary(
        related='company_id.logo',
        readonly=False
    )

    company_vat = fields.Char(
        related='company_id.vat',
        readonly=False
    )

    company_registry = fields.Char(
        related='company_id.company_registry',
        readonly=False
    )

    company_phone = fields.Char(
        related='company_id.phone',
        readonly=False
    )

    company_email = fields.Char(
        related='company_id.email',
        readonly=False
    )

    company_website = fields.Char(
        related='company_id.website',
        readonly=False
    )

    website_name = fields.Char(
        related='website_id.name',
        readonly=False
    )

    fetchmail_server_id = fields.Many2one(
        comodel_name='fetchmail.server',
        string='Incoming Mail Server'
    )

    ir_mail_server_id = fields.Many2one(
        comodel_name='ir.mail_server',
        string='Outgoing Mail Server'
    )

    social_twitter = fields.Char(related='website_id.social_twitter', readonly=False)
    social_facebook = fields.Char(related='website_id.social_facebook', readonly=False)
    social_linkedin = fields.Char(related='website_id.social_linkedin', readonly=False)
    social_youtube = fields.Char(related='website_id.social_youtube', readonly=False)
    social_instagram = fields.Char(related='website_id.social_instagram', readonly=False)
    theme_module_ids = fields.Many2many(comodel_name='ir.module.module', compute='_get_theme_module_ids')

    def _reopen_self(self):
        action = super()._reopen_self()
        action['name'] = _('Welcome to Odoo')
        return action

    def _get_theme_module_ids(self):
        for wizard in self:
            wizard.theme_module_ids = self.env['ir.module.module'].search(
                [
                    ('state', '!=', 'uninstallable'),
                    ('category_id', 'not in', [
                        self.env['ir.model.data']._xmlid_to_res_id('base.module_category_hidden'),
                        self.env['ir.model.data']._xmlid_to_res_id('base.module_category_theme_hidden'),
                    ]),
                    '|',
                    ('category_id', '=', self.env['ir.model.data']._xmlid_to_res_id('base.module_category_theme')),
                    ('category_id.parent_id', '=', self.env['ir.model.data']._xmlid_to_res_id('base.module_category_theme'))
                ]
            )

    @api.model
    def _selection_state(self):
        return [
            ('start', 'Company Information'),
            ('website', 'Website'),
            ('theme', 'Theme'),
            ('mailing', 'Mailing'),
            ('final', 'Final'),
        ]

    def state_exit_start(self):
        self.state = 'website'

    def state_exit_website(self):
        self.state = 'theme'

    def state_exit_theme(self):
        self.state = 'mailing'

    def state_exit_mailing(self):
        onboarding_group = self.env.ref('base_onboarding.onboarding_group')
        onboarding_group.sudo().write({
            'users': [(3, self.env.user.id, 0)]
        })
        self.state = 'final'

    def state_previous_mailing(self):
        self.state = 'theme'

    def state_previous_theme(self):
        self.state = 'website'

    def state_previous_website(self):
        self.state = 'start'

    def skip_to_end(self):
        self.ensure_one()
        self.state_exit_mailing()
        return self._reopen_self()

