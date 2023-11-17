from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Appartement(models.Model):
    _name = 'realtor.appartment' 
    _description = 'Appartement'

    # un nom unique
    name = fields.Char(string='Nom', required=True, index=True, copy=False, default='New')
    # une description textuelle de l’appartement
    description = fields.Text(string='Description')
    # une photo de l’appartement
    photo = fields.Binary(string='Photo')
    # une date de disponibilité, minimum 3 mois après la création de l’appartement dans le module
    availability = fields.Datetime(string='Date de disponibilité', default=fields.Date.today)
    # le prix attendu (strictement supérieur à 0)
    price = fields.Float(string='Prix attendu', required=True, default=0.0)
    # la surface de l’appartement (strictement supérieure à 0)
    surface = fields.Integer(string='Surface de l\'appartement', required=True, default=0)
    # la surface de la terrasse (supérieure ou égale à 0)
    terrace_surface = fields.Integer(string='Surface de la terrasse', required=True, default=0)
    # la surface totale, calculée à partir des surfaces précédentes
    total_surface = fields.Integer(string='Surface totale', compute='_compute_total_surface')
    # l’acheteur ayant fait la meilleure offre
    best_offer_buyer = fields.Many2one('res.partner', string='Meilleur Acheteur')
    # le montant de la meilleure offre, ce montant doit au minimum être de 90%, du prix attendu
    best_offer_amount = fields.Float(string='Montant de la meilleure offre')

    prodcut_id = fields.Many2one('product.template', string='Produit associé')

    @api.depends('surface', 'terrace_surface')
    def _compute_total_surface(self):
        for appartement in self:
            appartement.total_surface = appartement.surface + appartement.terrace_surface

    @api.constrains('best_offer_amount')
    def check_best_offer(self):
        for appartement in self:
            if appartement.best_offer_amount < 0.9 * appartement.price:
                raise ValidationError("Le montant de l\'offre doit être au minimum de 90% du prix attendu de l'appartement")

    @api.constrains('availability')
    def check_free_date(self):
        for appartement in self:
            if appartement.availability < appartement.create_date + timedelta(days=90):
                raise ValidationError("La date de disponibilité doit être au minimum de 3 mois après la création de l'appartement dans le module")

    @api.constrains('price')
    def check_price(self):
        for appartement in self:
            if appartement.price <= 0:
                raise ValidationError("Le prix attendu doit être strictement supérieur à 0")

    @api.constrains('surface')
    def check_surface(self):
        for appartement in self:
            if appartement.surface <= 0:
                raise ValidationError("La surface doit être strictement supérieure à 0")

    @api.constrains('terrace_surface')
    def check_terrace_surface(self):
        for appartement in self:
            if appartement.surface < 0:
                raise ValidationError("La surface de la terrasse doit être supérieure à 0")

    _sql_constraints = [
            ('name_unique',
            'UNIQUE(name)',
            "The appartment's name must be unique"),
        ]


