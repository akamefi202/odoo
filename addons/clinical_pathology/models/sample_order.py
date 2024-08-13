from odoo import models, fields
from odoo.exceptions import UserError


class SampleOrder(models.Model):
    _name = 'cp.sample_order'
    _description = 'cp_sample_order'

    study_id = fields.Many2one(
        comodel_name='study.study',
        string="Associate Study",
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
        if self.study_id is None:
            raise UserError("Please select a study first.")
        if len(self.study_id.group_ids) == 0:
            raise UserError("The study has no groups. Please create groups first.")

        dialog = self.env['cp.group_selection_dialog'].create({
            'study_group_ids': self.study_id.group_ids,
            'sample_order_id': self.id,
            'animal_id': self.study_id.animal_id.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Group Selection Dialog',
            'res_model': 'cp.group_selection_dialog',
            'view_mode': 'form',
            'target': 'new',
            'res_id': dialog.id
        }
