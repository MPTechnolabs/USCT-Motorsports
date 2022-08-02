# -*- coding: utf-8 -*-

from odoo import fields, api, models, tools, _
from random import randint
import warnings
from odoo.osv import expression


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    attribute_visibility = fields.Selection([('visible', 'Visible'), ('hidden', 'Hidden')], default='visible', string="Attribute Info Display")

    @api.onchange('attribute_visibility')
    def onchange_attribute_visibility(self):
        if self.attribute_visibility == 'hidden':
            if self.create_variant == 'always' or self.create_variant == 'dynamic': 
                return {
                    'warning': {
                        'title': _('Attribute Info Display.'),
                        'message': _("When Varient Creation mode is Instantly or Dynamically, then you can not sent hidden into Attribute Info Display.")
                    }
                }


    @api.model
    def create(self, vals):
        res = super(ProductAttribute, self).create(vals)
        if res.attribute_visibility == 'hidden':
            if res.create_variant == 'always' or res.create_variant == 'dynamic': 
                res.attribute_visibility = 'visible'  
        return res

    def write(self, vals):
        if vals.get('create_variant', False) and vals.get('create_variant', '') in ['always', 'dynamic']:
            if self.attribute_visibility == 'hidden' and vals.get('attribute_visibility') != 'hidden':
                self.attribute_visibility = 'visible'  
        if vals.get('attribute_visibility', '') == 'hidden':
            if self.create_variant in ['always', 'dynamic'] and vals.get('create_variant', '') != 'no_variant': 
                self.attribute_visibility = 'visible'  
                return {
                    'warning': {
                        'title': _('Attribute Info Display.'),
                        'message': _("When Varient Creation mode is Instantly or Dynamically, then you can not sent hidden into Attribute Info Display.")
                    }
                }
        res = super(ProductAttribute, self).write(vals)
        return res