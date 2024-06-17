from odoo import models, fields


class Protocol(models.Model):
    _name = 'ar.protocol'
    _description = 'ar_protocol'

    animal_ids = fields.One2many(
        comodel_name="study.animal",
        string="Animals",
    )
