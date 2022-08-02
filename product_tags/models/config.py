# -*- coding: utf-8 -*-''
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class website(models.Model):
    _inherit = 'website'

    product_tag_website = fields.Boolean("Product Tags on Website", default=False)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_tag_website = fields.Boolean("Product Tags on Website", default=False)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.website_id.write({'product_tag_website': self.product_tag_website})
        return res 

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        website_id  =self.website_id
        if not website_id:
            website_id = self.env['website'].search([], limit=1)
        res.update(product_tag_website=website_id.product_tag_website)
        return res 
