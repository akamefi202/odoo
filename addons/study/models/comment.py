from odoo import models, fields


class Comment(models.Model):
    _name = 'study.comment'
    _description = 'study_comment'

    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    study_id = fields.Many2one("study.study", string="Study")
    text = fields.Char(string="Text")
