# -*- coding: utf-8 -*-
{
    'name': "Project Cars Enhancement",
    'summary': """
        Project Cars Enhancement.""",
    'description': """
        Project Cars Enhancement.
    """,
    'author': "MP Technolabs",
    'website': "https://www.mptechnolabs.com/",
    'category': 'product ',
    'version': '15.0.1.6',
    'depends': ['web', 'sale_management', 'product', 'website_sale', 'mrp'],
    'data': [
        'views/template.xml',
        'views/product_attribute_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'project_cars_enhancement/static/src/scss/product.scss',
            'project_cars_enhancement/static/src/js/VariantMixin.js',   
        ],
    },
}
