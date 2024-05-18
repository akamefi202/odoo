from odoo import models, fields


class Subgroup(models.Model):
    _name = 'study.subgroup'
    _description = 'study_subgroup'

    group_id = fields.Many2one(comodel_name="study.group", string="Group", required=True, default=lambda self: self.env['study.group'])
    male_animal_count = fields.Integer(string="Male Animal Count", default=0)
    female_animal_count = fields.Integer(string="Female Animal Count", default=0)
