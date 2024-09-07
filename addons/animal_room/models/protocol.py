from odoo import models, fields, api
from odoo.exceptions import UserError
import uuid
import random


class Protocol(models.Model):
    _name = 'ar.protocol'
    _description = 'ar_protocol'
    #_sql_constraints = [('make study_id one2one', 'unique(study_id)', 'study_id must be unique to ensure one2one relationship')]

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

    grouping_method = fields.Selection(
        string="Grouping Method",
        selection=[('random', 'Random Grouping'), ('average', 'Auto Grouping based on Average Weight')],
        default="random",
        required=True,
    )

    def _compute_display_name(self):
        for protocol in self:
            protocol.display_name = protocol.study_id.name

    @api.onchange('study_id')
    def get_study_data(self):
        if self.study_id:
            self.animal_name = self.study_id.animal_id.name
            self.animal_number_total = self.study_id.animal_number_total
            self.animal_number_per_cage = self.study_id.animal_number_per_cage
            self.study_end_date = self.study_id.end_date

    def allocate_subjects(self):
        print("allocate_subjects")
        if len(self.subject_ids) != 0 and self.subjects_allocated is True:
            raise UserError("Subjects are allocated already. Please delete all allocated subjects to reallocate.")

        subjects = []
        for i in range(self.animal_number_total):
            subjects.append([0, 0, {
                'uai': '',
                'sex': 'Male',
                'animal_name': self.animal_name,
                'protocol_id': self.id,
                'study_id': self.study_id.id,
                'alive': 'alive',
                'segment_id': i + 1,
            }])

        self.write({'subject_ids': subjects})
        self.subjects_allocated = True
        self.uai_assigned = False

    def assign_uai(self):
        print("assign_uai")
        if self.uai_assigned is True:
            raise UserError("UAIs are assigned already.")

        for subject in self.subject_ids:
            subject.write({'uai': uuid.uuid1()})

        self.uai_assigned = True

    def grouping_subjects(self):
        print("grouping_subjects")
        #if self.subjects_allocated is False or len(self.subject_ids) == 0:
        #    raise UserError("Subjects are not allocated yet.")

        # get animal count to be grouped
        animal_number_grouped = 0
        group_ids = self.study_id.group_ids
        for g in group_ids:
            animal_number_grouped += (g.male_animal_count + g.female_animal_count)
            if g.have_subgroup:
                animal_number_grouped += (g.subgroup_male_animal_count + g.subgroup_female_animal_count)

        if self.animal_number_total != animal_number_grouped:
            raise UserError('Total animal count of Groups doesn\'t match with \'total number of Subjects\'.')

        if self.grouping_method == 'random':
            # Random grouping
            self.random_grouping_subjects()
        else:
            # Auto grouping based on average weight
            self.average_grouping_subjects()

    def random_grouping_subjects(self):
        print('random_grouping_subjects')
        number_array = []
        random_number_array = []
        group_index_array = []

        # get number array in random order that consists of numbers between 0-n
        for i in range(self.animal_number_total):
            number_array.append(i)
        for i in range(self.animal_number_total):
            random_index = random.randint(0, len(number_array) - 1)
            random_number_array.append(number_array[random_index])
            number_array.pop(random_index)

        # get array of group index in ascending order (0-n)
        group_ids = self.study_id.group_ids
        group_index = 0
        for g in group_ids:
            group_animal_count = g.male_animal_count + g.female_animal_count
            if g.have_subgroup:
                group_animal_count += (g.subgroup_male_animal_count + g.subgroup_female_animal_count)

            for i in range(group_animal_count):
                group_index_array.append(group_index)
            group_index += 1

        # allocate group ids to subjects in random order
        for i in range(self.animal_number_total):
            random_group_index = group_index_array[random_number_array[i]]
            self.subject_ids[i].group_id = group_ids[random_group_index]

    def average_grouping_subjects(self):
        print('average_grouping_subjects')
        bodyweight_array = []
        subject_index_array = []
        subject_ids = self.subject_ids
        subject_count = len(subject_ids)
        group_ids = self.study_id.group_ids
        group_count = len(group_ids)

        # get bodyweight array in descending order
        for i, s in enumerate(subject_ids):
            # get bodyweight of subject
            bodyweight_value = 0
            for r in reversed(s.record_ids):
                if r.category_name == 'Bodyweight':
                    bodyweight_value = r.value
                    break

            bodyweight_array.append(bodyweight_value)
            subject_index_array.append(i)

        for i in range(subject_count - 1):
            for j in range(i + 1, subject_count):
                if bodyweight_array[i] < bodyweight_array[j]:
                    bodyweight_array[i], bodyweight_array[j] = bodyweight_array[j], bodyweight_array[i]
                    subject_index_array[i], subject_index_array[j] = subject_index_array[j], subject_index_array[i]

        # rearrange group ids to ensure average value
        group_average_array = []
        group_count_array = []
        group_cur_count_array = []
        group_index_array = [0] * subject_count
        for g in group_ids:
            group_average_array.append(0)
            group_cur_count_array.append(0)

            group_animal_count = g.male_animal_count + g.female_animal_count
            if g.have_subgroup:
                group_animal_count += (g.subgroup_male_animal_count + g.subgroup_female_animal_count)
            group_count_array.append(group_animal_count)

        for i in range(subject_count):
            group_index = 0
            # get index of group with minimum average value and still have a gap
            for j in range(1, group_count):
                if group_cur_count_array[group_index] >= group_count_array[group_index]:
                    group_index = j
                    continue
                if (group_average_array[j] < group_average_array[group_index] and
                        group_cur_count_array[j] < group_count_array[j]):
                    group_index = j
                    continue
            group_index_array[subject_index_array[i]] = group_index
            group_average_array[group_index] += 0 if group_count_array[group_index] == 0\
                else bodyweight_array[i] / group_count_array[group_index]
            group_cur_count_array[group_index] += 1

        # allocate group ids to subjects in calculated order
        for i in range(subject_count):
            group_index = group_index_array[i]
            self.subject_ids[i].group_id = group_ids[group_index]
