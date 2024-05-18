from odoo import models, fields


class Article(models.Model):
    _name = 'study.article'
    _description = 'study_article'

    name = fields.Char(required=True, string="Name")
    total_amount = fields.Float(required=True, string="Total Amount")
