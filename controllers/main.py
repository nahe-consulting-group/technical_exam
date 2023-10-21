from odoo import http
from odoo.http import request
import json


class CreditGroupController(http.Controller):
    @http.route(
        "/api/credit_group", type="json", auth="public", methods=["POST"], csrf=False
    )
    def create_or_update_credit_group(self, **kwargs):
        data = request.jsonrequest
        credit_groups = data.get("grupo_credititos", [])

        response = {"status": 200, "message": "OK"}

        for group_data in credit_groups:
            canal_code = group_data.get("canal")
            sales_channel = (
                request.env["sales.channel"].sudo().search([("code", "=", canal_code)])
            )

            if not sales_channel:
                response["status"] = 400
                response["message"] = "No se encontró el canal {}".format(canal_code)
                return response

            credit_group = (
                request.env["credit.group"]
                .sudo()
                .search([("code", "=", group_data.get("codigo"))])
            )

            vals = {
                "name": group_data.get("name"),
                "code": group_data.get("codigo"),
                "sales_channel_id": sales_channel.id,
                "global_credit": group_data.get("credito_global"),
            }

            if credit_group:
                credit_group.write(vals)
            else:
                request.env["credit.group"].sudo().create(vals)

        return response
