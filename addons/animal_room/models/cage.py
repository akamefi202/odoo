from odoo import models, fields


class Cage(models.Model):
    _name = 'ar.cage'
    _description = 'ar_cage'

    name = fields.Char(required=True, string="Name")
    room_id = fields.Many2one(comodel_name="ar.room", string="Room", required=True)

    def move_to_cage(self):
        cage_form = self.env.ref('animal_room.ar_cage_form_view', False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ar.cage',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': cage_form.id,
        }
