from odoo import models, fields, api, exceptions

class InheritEstateModel(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        self.env['account.move'].create({
            'partner_id': self.buyer_id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                ({
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price*0.06,
                }),
                ({
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': 100,
                })
            ]
        })
        return super().action_sold()