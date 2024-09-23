from odoo import models, fields, api


class SampleSubject(models.Model):
    _name = 'cp.sample_subject'
    _description = 'cp_sample_subject'

    uai = fields.Char(string="Unique Animal ID", readonly=True, default="N/A")
    sex = fields.Char(string="Sex", readonly=True, default="N/A")
    animal_name = fields.Char(string="Animal Name", readonly=True, default="N/A")
    animal_number = fields.Char(string="Animal Number", readonly=True, default="N/A")
    group_name = fields.Char(string="Group Name", readonly=True, default="N/A")
    mortality = fields.Char(string="Mortality", readonly=True, default="N/A")
    # selected bool value for subject selection dialog of clinical pathology module
    selected = fields.Boolean(string="Selected", default=False)

    sample_order_id = fields.Many2one(comodel_name="cp.sample_order", required=True, ondelete="cascade")
