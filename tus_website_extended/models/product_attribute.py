# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    
    show_all_attribute_values = fields.Boolean('Show All Attribute Values', copy=False)
    is_default_filter = fields.Boolean('Is Default Filter?', copy=False)