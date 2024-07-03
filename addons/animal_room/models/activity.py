from odoo import models, fields


class Activity(models.Model):
    _name = 'ar.activity'
    _description = 'ar_activity'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
    category_id = fields.Many2one(
        comodel_name='ar.category',
        string="Category",
        required=True)
    measurement_ids = fields.Many2many(
        comodel_name="ar.measurement",
        string="Measurements",
    )
