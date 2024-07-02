from odoo import models, fields


class Category(models.Model):
    _name = 'ar.category'
    _description = 'ar_category'

    name = fields.Char(string="Name", required=True)
    abbreviation = fields.Char(string="Abbreviation")
    tag_ids = fields.Many2many(
        comodel_name="ar.tag",
        string="Tags",
    )
