from odoo import models, fields, api


class Subject(models.Model):
    _name = 'ar.subject'
    _description = 'ar_subject'

    uai = fields.Char(string="Unique Animal ID", required=True, readonly=True)
    sex = fields.Char(string="Sex", required=True, readonly=True)
    animal_name = fields.Char(string="Animal Name", compute="get_animal_name", required=True, readonly=True)
    protocol_id = fields.Many2one(comodel_name="ar.protocol", string="Protocol", required=True)
    group_id = fields.Many2one(
        comodel_name='study.group',
        string="Group")
    cage_id = fields.Many2one(
        comodel_name='ar.cage',
        string="Cage")

    @api.depends('protocol_id')
    def get_animal_name(self):
        if self.protocol_id:
           self.animal_name = self.protocol_id.animal_name


