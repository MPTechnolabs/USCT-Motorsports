# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        """Override for website, where we want to:
            - take the website pricelist if no pricelist is set
            - apply the b2b/b2c setting to the result

        This will work when adding website_id to the context, which is done
        automatically when called from routes with website=True.
        """
        self.ensure_one()

        current_website = False

        if self.env.context.get('website_id'):
            current_website = self.env['website'].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()
        res = super(ProductTemplate, self)._get_combination_info(combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist, parent_combination=parent_combination, only_template=only_template)
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if self.env.context.get('website_id'):
            context = dict(self.env.context, ** {
                'quantity': self.env.context.get('quantity', add_qty),
                'pricelist': pricelist and pricelist.id
            })

            product = (self.env['product.product'].browse(combination_info['product_id']) or self).with_context(context)
            res.update({'default_code': product.default_code and product.default_code or ''})
            mrp_bom_id = self.env['mrp.bom'].search([('product_id', '=', product.id), ('type', '=', 'phantom')])
            mrp_data = []
            mrp_data_count = 0
            final_total = 0
            for bom_line_id in mrp_bom_id.bom_line_ids:
                mrp_data_count += 1
                final_total += round(bom_line_id.product_qty * bom_line_id.product_id.list_price, 2)
                mrp_data.append({
                    'component': bom_line_id.product_id.name,
                    'quantity': bom_line_id.product_qty,
                    'unit': bom_line_id.product_uom_id.name,
                    'list_price': round(bom_line_id.product_id.list_price, 2),
                    'total': round(bom_line_id.product_qty * bom_line_id.product_id.list_price, 2),
                    })

            res.update({'mrp_bom': mrp_bom_id and mrp_bom_id or False, 
                'mrp_data': mrp_data, 'mrp_data_count': mrp_data_count,
                'final_total': round(final_total, 2),
                'save_price' : 'Save: ' + str(round(product.list_price - final_total, 2)) })

        return res