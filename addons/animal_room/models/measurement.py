from odoo import models, fields


class Measurement(models.Model):
    _name = 'ar.measurement'
    _description = 'ar_measurement'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation", required=True)
    unit_id = fields.Many2one(
            comodel_name='ar.unit',
            string="Unit",
            required=True)
    tag_ids = fields.Many2many(
        comodel_name="ar.tag",
        string="Tags",
    )

    def move_to_measurement(self):
        measurement_form = self.env.ref('animal_room.ar_measurement_form_view', False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ar.measurement',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': measurement_form.id,
        }
