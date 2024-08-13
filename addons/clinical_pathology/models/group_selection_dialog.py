from odoo import fields, models


class GroupSelectionDialog(models.Model):
    _name = "cp.group_selection_dialog"
    _description = 'cp_group_selection_dialog'

    study_group_ids = fields.Many2many(comodel_name='study.group', required=True)
    sample_order_id = fields.Many2one(comodel_name='cp.sample_order', required=True, ondelete="cascade")
    animal_id = fields.Many2one(comodel_name='study.animal', required=True)

    def select_group(self):
        print("select_group")
        for g in self.study_group_ids:
            for i in range(g.male_animal_count + g.female_animal_count):
                self.env['cp.sample'].create({
                    'sample_order_id': self.sample_order_id.id,
                    'animal_id': self.animal_id.id,
                    'group_id': g.id,
                })

        return self.study_group_ids
