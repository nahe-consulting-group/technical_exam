from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditGroup(models.Model):
    _name = "credit.group"
    _description = "Credit Group"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)
    code = fields.Char(string="Code", required=True, tracking=True)
    sales_channel_id = fields.Many2one(
        "sales.channel", string="Sales Channel", required=True, tracking=True
    )
    global_credit = fields.Monetary(
        string="Global Credit",
        currency_field="company_currency_id",
        required=True,
        tracking=True,
    )
    used_credit = fields.Monetary(
        string="Used Credit",
        currency_field="company_currency_id",
        compute="_compute_used_credit",
        store=True,
    )
    available_credit = fields.Monetary(
        string="Available Credit",
        currency_field="company_currency_id",
        compute="_compute_available_credit",
        store=True,
    )
    partner_ids = fields.Many2many(
        "res.partner",
        string="Partners",
        relation="credit_group_res_partner_rel",
        column1="credit_group_id",
        column2="partner_id",
        tracking=True,
    )
    company_currency_id = fields.Many2one(
        "res.currency",
        string="Company Currency",
        compute="_compute_company_currency",
        store=True,
    )
    _sql_constraints = [
        ("code_uniq", "unique (code)", "The code of the credit group must be unique!")
    ]

    def write(self, vals):
        # Si se actualiza partner_ids, verifica y actualiza credit_group_ids en res.partner
        if "partner_ids" in vals:
            for command in vals["partner_ids"]:
                if (
                    command[0] == 3
                ):  # 3 es el comando para eliminar un registro en O2M/M2M
                    partner = self.env["res.partner"].browse(command[1])
                    partner.credit_group_ids = False
        return super().write(vals)

    @api.model
    def _compute_company_currency(self):
        for record in self:
            record.company_currency_id = (
                self.env["res.company"]._get_main_company().currency_id
            )

    @api.depends("global_credit", "partner_ids")
    def _compute_used_credit(self):
        for group in self:
            # Get the company's currency
            company_currency = self.env.company.currency_id

            # 1. Total of confirmed sales not yet invoiced
            sales_domain = [
                ("state", "=", "sale"),
                ("invoice_status", "=", "to invoice"),
                ("partner_id", "in", group.partner_ids.ids),
            ]
            sales = self.env["sale.order"].search(sales_domain)
            total_sales = sum(
                sale.currency_id._convert(
                    sale.amount_total,
                    company_currency,
                    self.env.company,
                    sale.date_order,
                )
                for sale in sales
            )

            # 2. Total of unpaid invoices
            invoice_domain = [
                ("state", "=", "posted"),
                ("payment_state", "!=", "paid"),
                ("partner_id", "in", group.partner_ids.ids),
                ("move_type", "=", "out_invoice"),
            ]
            invoices = self.env["account.move"].search(invoice_domain)
            total_invoices = sum(
                invoice.currency_id._convert(
                    invoice.amount_total,
                    company_currency,
                    self.env.company,
                    invoice.invoice_date,
                )
                for invoice in invoices
            )

            # Set the value of used credit
            group.used_credit = total_sales + total_invoices

    @api.depends("global_credit", "used_credit")
    def _compute_available_credit(self):
        for group in self:
            group.available_credit = group.global_credit - group.used_credit
