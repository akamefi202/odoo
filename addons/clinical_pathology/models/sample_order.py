from odoo import models, fields, api
from odoo.exceptions import UserError


class SampleOrder(models.Model):
    _name = 'cp.sample_order'
    _description = 'cp_sample_order'

    protocol_id = fields.Many2one(
        comodel_name='ar.protocol',
        string="Associate Protocol",
        required=True
    )
    old_protocol_id = fields.Many2one(
        comodel_name='ar.protocol',
        string="Old Associate Protocol",
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

    sample_subject_ids = fields.One2many(
        comodel_name='cp.sample_subject',
        inverse_name='sample_order_id'
    )

    def get_sample_subjects(self):
        if self.protocol_id and self.protocol_id != self.old_protocol_id:
            print('get_sample_subjects')
            subject_ids = self.protocol_id.subject_ids

            # delete original sample subjects
            for s in self.sample_subject_ids:
                s.unlink()

            # create new sample subjects
            for s in subject_ids:
                self.env['cp.sample_subject'].create({
                    'uai': s.uai,
                    'sex': s.sex,
                    'animal_name': s.animal_name,
                    'group_name': s.group_id.name,
                    'mortality': 'Alive' if s.alive == 'alive' else 'Dead',
                    'sample_order_id': self._origin.id,
                })

            self.old_protocol_id = self.protocol_id
            self.env.cr.commit()

    def collect_samples(self):
        print("collect_samples")

        if len(self.sample_ids) != 0:
            raise UserError("Samples are collected already. Please delete all collected samples first.")
        if self.protocol_id is None:
            raise UserError("Please select a protocol first.")
        if len(self.protocol_id.subject_ids) == 0:
            raise UserError("The protocol has no subjects. Please allocate subjects first.")

        for s in self.sample_subject_ids:
            if s.selected:
                self.env['cp.sample'].create({
                    'sample_order_id': self._origin.id,
                    'animal_name': s.animal_name,
                    'group_name': s.group_name,
                })

        self.env.cr.commit()

        # dialog = self.env['cp.subject_selection_dialog'].create({
        #     'sample_subject_ids': self.protocol_id.subject_ids,
        #     'sample_order_id': self.id,
        #     'animal_id': self.protocol_id.study_id.animal_id.id,
        # })
        # dialog = self.env['cp.subject_selection_dialog'].create({
        #     'subject_ids': self.protocol_id.subject_ids,
        #     'sample_order_id': self.id,
        #     'animal_id': self.protocol_id.study_id.animal_id.id,
        # })
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Subject Selection Dialog',
        #     'res_model': 'cp.subject_selection_dialog',
        #     'view_mode': 'form',
        #     'target': 'new',
        #     'res_id': dialog.id
        # }

    def delete_samples(self):
        print("collect_samples")

        for s in self.sample_ids:
            s.unlink()
