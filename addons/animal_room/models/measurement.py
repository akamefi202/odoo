from odoo import models, fields


class Measurement(models.Model):
    _name = 'ar.measurement'
    _description = 'ar_measurement'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
    unit_id = fields.Many2one(
            comodel_name='ar.unit',
            string="Unit",
            required=True)
