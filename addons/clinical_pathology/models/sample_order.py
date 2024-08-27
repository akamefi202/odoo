from odoo import models, fields
from odoo.exceptions import UserError


class SampleOrder(models.Model):
    _name = 'cp.sample_order'
    _description = 'cp_sample_order'

    protocol_id = fields.Many2one(
        comodel_name='ar.protocol',
        string="Associate Protocol",
        required=True
    )
    activity_id = fields.Many2one(
        comodel_name='ar.activity',
        string="Activity",
        required=True
    )
    instrument_id = fields.Many2one(
        comodel_name='ar.instrument',
        string="Instrument",
        required=True
    )
    sample_type = fields.Selection(
        string="Sample Type",
        selection=[('serum', 'Serum'), ('plasma', 'Plasma')],
        required=True
    )
    sample_ids = fields.One2many(
        comodel_name="cp.sample",
        string="Samples",
        inverse_name="sample_order_id",
    )

    def collect_samples(self):
        print("collect_samples")

        if len(self.sample_ids) != 0:
            raise UserError("Samples are collected already. Please delete all collected samples first.")
        if self.protocol_id is None:
            raise UserError("Please select a protocol first.")
        if len(self.protocol_id.subject_ids) == 0:
            raise UserError("The protocol has no subjects. Please allocate subjects first.")

        # dialog = self.env['cp.subject_selection_dialog'].create({
        #     'sample_subject_ids': self.protocol_id.subject_ids,
        #     'sample_order_id': self.id,
        #     'animal_id': self.protocol_id.study_id.animal_id.id,
        # })
        dialog = self.env['cp.subject_selection_dialog'].create({
            'subject_ids': self.protocol_id.subject_ids,
            'sample_order_id': self.id,
            'animal_id': self.protocol_id.study_id.animal_id.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subject Selection Dialog',
            'res_model': 'cp.subject_selection_dialog',
            'view_mode': 'form',
            'target': 'new',
            'res_id': dialog.id
        }

    def delete_samples(self):
        print("collect_samples")

        for s in self.sample_ids:
            s.unlink()
