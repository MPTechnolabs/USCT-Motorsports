# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    import_id = fields.Integer(string="File ID")