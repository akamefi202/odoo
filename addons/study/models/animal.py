from odoo import models, fields


class Animal(models.Model):
    _name = 'study.animal'
    _description = 'study_animal'

    name = fields.Char(required=True, string="Name")
    total_number = fields.Integer(string="Total Number")
