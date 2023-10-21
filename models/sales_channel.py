from odoo import models, fields, api


class SalesChannel(models.Model):
    _name = "sales.channel"
    _description = "Sales Channel"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(
        string="Code",
        readonly=True,
        copy=False,
        default=lambda self: self.env["ir.sequence"].next_by_code("sales.channel"),
    )
    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse", tracking=True)
    journal_id = fields.Many2one("account.journal", string="Journal", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = self.env["ir.sequence"].next_by_code("sales.channel") or "/"
        return super(SalesChannel, self).create(vals)
