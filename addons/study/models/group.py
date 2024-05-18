from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class Group(models.Model):
    _name = 'study.group'
    _description = 'study_group'

    study_id = fields.Many2one(comodel_name="study.study", string="Study", required=True)
    name = fields.Char(string="Name", required=True)
    article_amount = fields.Float(string="Test Article Amount", default=0)
    male_animal_count = fields.Integer(string="Male Animal Count", default=0)
    female_animal_count = fields.Integer(string="Female Animal Count", default=0)
    subgroup_ids = fields.One2many(
        comodel_name="study.subgroup",
        inverse_name="group_id",
        string="Study Sub-groups",
    )

    def move_to_group(self):
        group_form = self.env.ref('study.study_group_form_view', False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'study.group',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': group_form.id,
        }
