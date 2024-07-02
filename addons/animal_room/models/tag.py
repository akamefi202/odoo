from odoo import models, fields


class Unit(models.Model):
    _name = 'ar.tag'
    _description = 'ar_tag'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
