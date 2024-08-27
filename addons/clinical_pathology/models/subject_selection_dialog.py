from odoo import fields, models


class SubjectSelectionDialog(models.Model):
    _name = "cp.subject_selection_dialog"
    _description = 'cp_subject_selection_dialog'

    #sample_subject_ids = fields.Many2many(comodel_name='cp.sample_subject', required=True)
    subject_ids = fields.Many2many(comodel_name='ar.subject', required=True)
    sample_order_id = fields.Many2one(comodel_name='cp.sample_order', required=True, ondelete="cascade")
    animal_id = fields.Many2one(comodel_name='study.animal', required=True)

    def select_subject(self):
        print("select_group")
        #for s in self.sample_subject_ids:
        for s in self.subject_ids:
            self.env['cp.sample'].create({
                'sample_order_id': self.sample_order_id.id,
                'animal_id': self.animal_id.id,
                'group_id': s.group_id.id,
            })

        return True


    def add_subjects(self):
        print("add_subjects")

        # if len(self.sample_ids) != 0:
        #     raise UserError("Samples are collected already. Please delete all collected samples first.")
        # if self.protocol_id is None:
        #     raise UserError("Please select a protocol first.")
        # if len(self.protocol_id.subject_ids) == 0:
        #     raise UserError("The protocol has no subjects. Please allocate subjects first.")
        #
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
