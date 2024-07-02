from odoo import models, fields


class Unit(models.Model):
    _name = 'ar.unit'
    _description = 'ar_unit'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
