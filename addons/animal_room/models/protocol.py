from odoo import models, fields, api
import uuid


class Protocol(models.Model):
    _name = 'ar.protocol'
    _description = 'ar_protocol'

    study_id = fields.Many2one(
        comodel_name='study.study',
        string="Associate Study",
        required=True)
    animal_name = fields.Char(string="Animal")
    animal_number_total = fields.Integer(string="Animal Number")
    animal_number_per_cage = fields.Integer(string="Animal Number Per Cage")
    study_end_date = fields.Date(string="Study End Date")

    subjects_allocated = fields.Boolean(string="Subjects Allocated", default=False)
    uai_assigned = fields.Boolean(string="UAI Assigned", default=False)

    subject_ids = fields.One2many(
        comodel_name="ar.subject",
        string="Subjects",
        inverse_name="protocol_id",
    )

    @api.onchange('study_id')
    def get_study_data(self):
        if self.study_id:
            self.animal_name = self.study_id.animal_name
            self.animal_number_total = self.study_id.animal_number_total
            self.animal_number_per_cage = self.study_id.animal_number_per_cage
            self.study_end_date = self.study_id.end_date

    def allocate_subjects(self):
        print("Allocate Subjects")
        #if self.subjects_allocated == True:
        #    return

        #uuid.uuid1()
        subjects = []
        for i in range(self.animal_number_total):
            subjects.append([0, 0, {
                'uai': '',
                'sex': 'Male',
                'animal_name': self.animal_name,
                'protocol_id': self.id
            }])

        self.write({'subject_ids': subjects})
        self.subjects_allocated = True

    def assign_uai(self):
        print("Assign UAI")
        #if self.uai_assigned == True
        #    return

        for subject in self.subject_ids:
            subject.write({'uai': uuid.uuid1()})

        self.uai_assigned = True
