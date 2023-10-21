{
    ###########################
    # Delete all the commented lines after editing the module
    ###########################
    "name": "Technical Exam - Mirgor",
    "summary": """
        Module meant to solve Mirgor's technical exam for a Senior Developer Position""",
    "author": "Nahe Consulting Group",
    "maintainers": ["nahe-consulting-group"],
    "website": "https://nahe.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "15.0.2.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": ["base", "sale", "account", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/sales_channel_views.xml",
        "views/sale_order_views.xml",
        "views/credit_group_views.xml",
        "views/stock_picking_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
        "reports/report_credit_group.xml",
        "reports/template_credit_group_report.xml",
    ],
    ### XML Demo files
    # only loaded in demo mode
    # "demo": [
    #     "demo/demo.xml",
    # ],
    ### Assets
    # In 15.0, Odoo adds a new way to add js/css assets files to a module.
    # https://www.holdenrehg.com/blog/2021-10-08_odoo-manifest-asset-bundles
    # "assets": {
    #     "web.assets_backend": [
    #         "/my_module/path/to/file"
    #     ],
    #     "web.assets_qweb": [
    #         "/my_module/path/to/file", # QWeb templates. Example: 'pos_sale/static/src/xml/**/*',
    #     ],
    # }
    ###########################
    # Delete all the commented lines after editing the module
    ###########################
}
