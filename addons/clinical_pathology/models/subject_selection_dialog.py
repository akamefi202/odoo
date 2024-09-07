from odoo import fields, models


class SubjectSelectionDialog(models.Model):
    _name = "cp.subject_selection_dialog"
    _description = 'cp_subject_selection_dialog'

    subject_ids = fields.Many2many(comodel_name='ar.subject', required=True)
    sample_order_id = fields.Many2one(comodel_name='cp.sample_order', required=True, ondelete="cascade")
    animal_id = fields.Many2one(comodel_name='study.animal', required=True)

    def select_subject(self):
        print("select_group")
        print(self.subject_ids[0].display_name)
        for s in self.subject_ids:
            self.env['cp.sample'].create({
                'sample_order_id': self.sample_order_id.id,
                'animal_id': self.animal_id.id,
                'group_id': s.group_id.id,
            })

        return True
