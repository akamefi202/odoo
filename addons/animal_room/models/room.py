from odoo import models, fields


class Room(models.Model):
    _name = 'ar.room'
    _description = 'ar_room'

    name = fields.Char(required=True, string="Name")
    code = fields.Char(required=True, string="ID")
    location = fields.Char(required=True, string="Location")
    pic_id = fields.Many2one(
        comodel_name='res.users',
        string="Person in Charge",
        store=True,
        readonly=False,
        index=True,
        required=True)
    comment = fields.Char(string="Comment")

    cage_ids = fields.One2many(
        comodel_name="ar.cage",
        inverse_name="room_id",
        string="Cages",
    )
