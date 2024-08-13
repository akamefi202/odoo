from odoo import models, fields


class Instrument(models.Model):
    _name = 'ar.instrument'
    _description = 'ar_instrument'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
    category_id = fields.Many2one(
        comodel_name='ar.category',
        string="Category",
        required=True
    )
    activity_ids = fields.Many2many(
        comodel_name="ar.activity",
        string="Activities",
    )
