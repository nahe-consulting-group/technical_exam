from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sales_channel_id = fields.Many2one(
        "sales.channel", string="Sales Channel", readonly=True, tracking=True
    )
