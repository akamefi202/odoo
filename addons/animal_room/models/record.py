from odoo import models, fields, api


class Record(models.Model):
    _name = 'ar.record'
    _description = 'ar_record'

    activity_id = fields.Many2one(
        comodel_name='ar.activity',
        string="Activity",
        required=True)
    value = fields.Float(
        string="Value",
        default=0,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        index=True,
        required=True
    )

    subject_id = fields.Many2one(
        comodel_name='ar.subject',
        string="Subject",
        required=True,
        ondelete="cascade"
    )
    category_name = fields.Char(
        string="Category Name",
        compute="get_category_name",
        readonly=True,
        store=True
    )

    @api.depends('activity_id')
    def get_category_name(self):
        if self.activity_id:
            self.category_name = self.activity_id.category_id.name
