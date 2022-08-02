# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.addons.website_sale.controllers.main import WebsiteSale as WS
from odoo.http import request


class WebsiteSale(WS):
    
    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super(WebsiteSale, self).shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)
        request_args = request.httprequest.args
        attrib_list = request_args.getlist('attrib')
        get_attrib_list = [i for i in attrib_list if i != '']
        if not get_attrib_list:
            attributes = request.env['product.attribute'].sudo().search([('is_default_filter', '=', True)])
            res.qcontext.update({'attributes':attributes})
        return res


    @http.route('/get_more_product_information', type='http', auth='public', website=True)
    def product_information(self, **post):

        value = {
            'product_name': post.get('product_name'),
            'product_id': post.get('product_id'),
            'return_url': post.get('return_url'),
        }
        return request.render('tus_website_extended.get_more_product_information_page',value )
