from odoo import models, fields


class Sample(models.Model):
    _name = 'cp.sample'
    _description = 'cp_sample'

    group_id = fields.Many2one(
        comodel_name='study.group',
        string="Group",
    )
    animal_id = fields.Many2one(
        comodel_name='study.animal',
        string="Animal",
    )
    sample_order_id = fields.Many2one(
        comodel_name="cp.sample_order",
        string="Sample Order",
        required=True,
        ondelete="cascade"
    )

    animal_name = fields.Char(string="Animal Name")
    group_name = fields.Char(string="Group")
