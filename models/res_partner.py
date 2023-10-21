from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    has_credit_control = fields.Boolean(string="Has Credit Control", default=False)
    credit_group_ids = fields.Many2many(
        "credit.group",
        string="Credit Groups",
        relation="credit_group_res_partner_rel",
        column1="partner_id",
        column2="credit_group_id",
    )

    @api.onchange("credit_group_ids")
    def _onchange_credit_group_ids(self):
        # Remove partners from unselected groups
        for group in self.credit_group_ids - self.credit_group_ids._origin:
            group.partner_ids = [(4, self.id)]

        # Add partners to selected groups
        for group in self.credit_group_ids._origin - self.credit_group_ids:
            group.partner_ids = [(3, self.id)]
