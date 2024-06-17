from odoo import models, fields


class Room(models.Model):
    _name = 'ar.room'
    _description = 'ar_room'

    name = fields.Char(required=True, string="Name")
    id = fields.Char(required=True, string="ID")
    location = fields.Char(required=True, string="Location")
    pic = fields.Char(required=True, string="Person in Charge")
    comment = fields.Char(string="Person in Charge")
