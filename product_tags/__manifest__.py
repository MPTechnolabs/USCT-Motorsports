# -*- coding: utf-8 -*-
{
    'name': "Product Tags",
    'summary': """
        Product Tags.""",
    'description': """
        Product Tags.
    """,
    'author': "MP Technolabs",
    'website': "https://www.mptechnolabs.com/",
    'category': 'product ',
    'version': '15.0.1.1',
    'depends': ['product', 'website_sale'],
    'data': [
        'views/product_tags.xml',
        'views/config_view.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'product_tags/static/src/scss/products.scss',
            
        ],
    },
}
