from odoo import models, fields, api


# inherited class from subject, which is for subject selection using checkboxes
class SampleSubject(models.Model):
    _name = 'cp.sample_subject'
    _description = 'cp_sample_subject'
    #_inherit = 'ar.subject'


    selected = fields.Boolean(string="", default="False")
