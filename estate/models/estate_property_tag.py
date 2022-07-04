from odoo import models, fields

class EstateTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name"

    name = fields.Char(string="Name")
    color = fields.Integer()

    _sql_constraints = [
        ('uniq_tag', 'UNIQUE(name)',
         'The name must be unique')
    ]
