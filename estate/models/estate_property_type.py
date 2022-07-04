from odoo import models, fields, api

class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name"

    name = fields.Char(string="Property Type")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_offer_count")
    sequence = fields.Integer()

    _sql_constraints = [
        ('uniq_type', 'UNIQUE(name)', 'The name must be unique')
    ]

    @api.depends("offer_ids")
    def _offer_count(self):
        self.offer_count = (len(self.offer_ids))