from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    appartment_id = fields.Many2one('realtor.appartment', string='Appartement associé', required=True)