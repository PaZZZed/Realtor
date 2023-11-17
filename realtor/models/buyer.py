from odoo import models, fields

class Buyer (models.Model):
    _inherit = 'res.partner'

    appartment_id = fields.One2many('realtor.appartment', 'best_offer_buyer', string='Appartement voulant être acheté')