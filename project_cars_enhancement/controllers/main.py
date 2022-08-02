# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.variant import VariantController 


class VariantController(VariantController):
    
    @http.route(['/sale/get_combination_info'], type='json', auth="user", methods=['POST'])
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        res = super(VariantController, self).get_combination_info(product_template_id, product_id, combination, add_qty, pricelist_id, **kw)
        product = request.env['product.product'].browse(int(res.get('product_id')))
        if product:
            mrp_bom_id = request.env['mrp.bom'].search([('product_id', '=', product.id), ('type', '=', 'phantom')])
            mrp_data = []
            mrp_data_count = 0
            final_total = 0
            for bom_line_id in mrp_bom_id.bom_line_ids:
                mrp_data_count +=1
                final_total += round(bom_line_id.product_qty * bom_line_id.product_id.list_price, 2)
                mrp_data.append({
                    'component': bom_line_id.product_id.name,
                    'quantity': bom_line_id.product_qty,
                    'list_price': round(bom_line_id.product_id.list_price, 2),
                    'unit': bom_line_id.product_uom_id.name,
                    'total': round(bom_line_id.product_qty * bom_line_id.product_id.list_price, 2),
                    })
                res.update({
                    'final_total': round(final_total, 2),
                    'save_price' : 'Save: ' + str(round(product.list_price - final_total, 2)),

                    })
            res.update({'mrp_bom': mrp_bom_id and mrp_bom_id or False, 'mrp_data': mrp_data, 'mrp_data_count': mrp_data_count})
        if product and product.default_code:
            res.update({'default_code': product.default_code and product.default_code or ''})
        return res
