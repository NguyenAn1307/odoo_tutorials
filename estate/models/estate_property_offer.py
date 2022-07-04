from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime

class EstateOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')])

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    validity = fields.Integer(string="Validity (days)", default="7")
    date_deadline = fields.Date(compute="_compute_deadline", string="Deadline") #, inverse="_inverse_deadline"

    _sql_constraints = [('price_check', 'CHECK(price > 0)', 'Offer price must be strictly positive')]

    # @api.depends("validity")
    # def _compute_validity(self):
    #     for record in self:
    #         dayOfMonth = record.date_deadline.strftime("%d")
    #         print(dayOfMonth)
    #         record.validity += dayOfMonth

    #
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if(record.create_date):
                record.date_deadline = record.create_date + relativedelta(days = record.validity)
            else :
                record.date_deadline = fields.Datetime.today() + relativedelta(days = record.validity)

    # def _inverse_deadline(self):
    #     for record in self:
    #         fmt = "%Y-%m-%d"
    #         d1 = str(record.date_deadline)
    #         d2 = str(fields.Datetime.now()).split(' ')[0]
    #         d1 = datetime.strptime(d1, fmt)
    #         print(d1)
    #         d2 = datetime.strptime(d2, fmt)
    #         # print(d1)
    #         # print(d2)
    #         if(record.create_date):
    #             record.validity = (record.date_deadline - record.create_date).days
    #         else:
    #             # record.validity = (datetime.strptime(str(record.date_deadline), fmt) - datetime.strptime(str(fields.Datetime.now()), fmt)).days
    #             record.validity = (d1-d2).days

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price == False:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
            else:
                if record.status == "accepted": return
                raise exceptions.UserError('Only one person can be accepted')

    def action_refuse(self):
        for record in self:
            if record.status == "refused":
                return
            if record.status == "accepted":
                record.property_id.selling_price = False
                record.property_id.buyer_id = False
            record.status = "refused"

    @api.model
    def create(self, vals):
        properties = self.env['estate.property'].browse(vals['property_id'])
        properties.state = 'offer_received'
        if vals['price'] < properties.best_price:
            raise exceptions.UserError("The offer must be higher %.2f" %(properties.best_price))
        else: return super(EstateOfferModel, self).create(vals)