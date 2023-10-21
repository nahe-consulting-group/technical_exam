from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    sales_channel_id = fields.Many2one(
        "sales.channel", string="Sales Channel", ondelete="restrict", store=True
    )

    # make sure we use the correct journal_id when posting
    def action_post(self):
        for move in self:
            if move.sales_channel_id:
                move.journal_id = move.sales_channel_id.journal_id
        return super(AccountMove, self).action_post()
