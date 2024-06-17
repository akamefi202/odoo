from odoo import models, fields


class Cage(models.Model):
    _name = 'ar.cage'
    _description = 'ar_cage'

    id = fields.Char(required=True, string="ID")
