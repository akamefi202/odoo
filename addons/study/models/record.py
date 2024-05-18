from odoo import models, fields


class Record(models.Model):
    _name = 'study.record'
    _description = 'study_record'

    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    study_id = fields.Many2one("study.study", string="Study")
    text = fields.Char(string="Text")
