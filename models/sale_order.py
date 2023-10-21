from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sales_channel_id = fields.Many2one(
        "sales.channel", string="Sales Channel", required=True, tracking=True
    )

    @api.onchange("sales_channel_id")
    def _onchange_sales_channel(self):
        if self.sales_channel_id:
            self.warehouse_id = self.sales_channel_id.warehouse_id

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        _logger.info("Preparing invoice, initial journal_id: %s", res.get("journal_id"))
        _logger.info(
            "Sales Channel: %s, Journal: %s",
            self.sales_channel_id,
            self.sales_channel_id.journal_id,
        )

        if self.sales_channel_id.journal_id:
            res["journal_id"] = self.sales_channel_id.journal_id.id
            _logger.info("Journal ID set to: %s", res["journal_id"])

        res["sales_channel_id"] = self.sales_channel_id.id
        return res

    # credit status to limit sales
    credit_status = fields.Selection(
        [
            ("no_limit", "No credit limit"),
            ("available", "Credit available"),
            ("blocked", "Credit blocked"),
        ],
        compute="_compute_credit_status",
        readonly=True,
        string="Credit Status",
        store=True,
    )

    @api.depends("partner_id", "sales_channel_id", "amount_total")
    def _compute_credit_status(self):
        for order in self:
            order.credit_status = "no_limit"
            if order.partner_id and order.sales_channel_id:
                credit_group = order.partner_id.credit_group_ids.filtered(
                    lambda g: g.sales_channel_id == order.sales_channel_id
                )
                if not credit_group:
                    order.credit_status = "blocked"
                    continue

                if order.amount_total > credit_group.available_credit:
                    order.credit_status = "blocked"
                else:
                    order.credit_status = "available"

    @api.onchange("partner_id", "sales_channel_id", "amount_total")
    def _onchange_credit_status(self):
        self._compute_credit_status()

    def action_confirm(self):
        # Verify credit_status
        if any(order.credit_status == "blocked" for order in self):
            raise UserError(
                _("You cannot confirm an order with blocked credit status.")
            )

        # Call original method
        res = super(SaleOrder, self).action_confirm()

        # Update values sales_channel_id
        for order in self:
            order.picking_ids.write({"sales_channel_id": order.sales_channel_id.id})

        return res
