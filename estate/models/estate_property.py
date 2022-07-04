from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Estate Model"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available Form", default=(fields.Datetime.today() + relativedelta(months = 3)), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True, default="0.00")
    selling_price = fields.Float(string="Selling Price", readonly=True, default="0.00", copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    living_area = fields.Integer(string="Living Area (sqm)", default="0")
    facades = fields.Integer(string="Facades", default="0")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default="0")
    garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string="Status", selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default="new")

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)", readonly=True, store=True)
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer", readonly=True, default="0.00", store=True)
    sequence = fields.Integer()

    _sql_constraints = [
        ('expected_price_check', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'),
        ('selling_price_check', 'CHECK(selling_price >= 0)', 'Selling price must be positive')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            price_list = record.offer_ids.mapped('price')
            if(len(price_list) != 0):
                record.best_price = max(price_list)
            else:
                record.best_price = 0.00

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = "east"
            # return {'warning': {
            #     'title': ("Warning"),
            #     'message': ('This option is not supported for Authorize.net')}}
        else:
            self.garden_area = ''
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state != "canceled":
                if record.state == "sold":
                    pass
                else: record.state = "sold"
            else:
                raise exceptions.UserError('Canceled property cannot be sold')

    def action_cancel(self):
        for record in self:
            if record.state != "sold":
                if record.state == "canceled":
                    pass
                else: record.state = "canceled"
            else:
                raise exceptions.UserError('Sold property cannot be canceled')

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price != False:
                if record.selling_price < (record.expected_price * 0.1):
                    raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price")

    def unlink(self):
        if self.state not in ('new', 'canceled'):
            raise exceptions.ValidationError("Only new and canceled properties can be delete ")
        return super().unlink()


    class InheriteUserModel(models.Model):
        _inherit = "res.users"

        property_ids = fields.One2many("estate.property", "salesperson_id")