# -*- coding: utf-8 -*-

from odoo import fields, models, tools
from random import randint

from odoo.osv import expression


class ProducttTags(models.Model):
    _name = "product.tags"
    _description = 'Product Tags'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string="Name")
    # bg_color = fields.Char(string='Tag background color', required=False,default=_get_default_color)
    # text_color = fields.Char(string='Tag text color', required=False, default=_get_default_color)

class ProductTemplate(models.Model):
    _inherit = 'product.product'

    product_tags_ids = fields.Many2many(comodel_name='product.tags', relation='product_variant_tags_rel', string='Tags')