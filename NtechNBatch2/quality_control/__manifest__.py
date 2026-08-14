{
    'name': "Quality Control",

    'summary': "QC Section Checking for product",

    'description': """
    Long description of module's purpose
    """,

    'author': "Ntech",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Ntech/',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account', 'website', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/quality_check_views.xml',
        'views/job_application_views.xml',
        'views/menu.xml',
        'views/stock_picking.xml',
        'views/website_templates.xml',
        'reports/quality_check_report.xml',
        'reports/invoice_report_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

