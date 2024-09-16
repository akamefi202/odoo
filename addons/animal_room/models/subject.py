from odoo import models, fields, api


class Subject(models.Model):
    _name = 'ar.subject'
    _description = 'ar_subject'

    uai = fields.Char(string="Unique Animal ID", readonly=True, default="N/A")
    sex = fields.Char(string="Sex", required=True, readonly=True)
    study_id = fields.Many2one(
        comodel_name='study.study',
        string="Associate Study",
        required=True,
        readonly=True,
    )
    animal_name = fields.Char(string="Animal Name", compute="get_animal_name", required=True, readonly=True)
    animal_number = fields.Char(string="Animal Number", readonly=True)
    protocol_id = fields.Many2one(comodel_name="ar.protocol", string="Protocol", required=True, ondelete="cascade")
    group_id = fields.Many2one(
        comodel_name='study.group',
        string="Group")
    cage_id = fields.Many2one(
        comodel_name='ar.cage',
        string="Cage")
    segment_id = fields.Integer(string="Segment Id", default=0)
    alive = fields.Selection(string="Dead or Alive", selection=[('dead', 'Dead'), ('alive', 'Alive')], default="alive")

    # bodyweight_record_ids = fields.Many2many(
    #     comodel_name="ar.record",
    #     string="Bodyweight Records",
    #     relation="subject_bodyweight_record_rel",
    # )
    # food_record_ids = fields.Many2many(
    #     comodel_name="ar.record",
    #     string="=Food Records",
    #     relation="subject_food_record_rel",
    # )
    # water_record_ids = fields.Many2many(
    #     comodel_name="ar.record",
    #     string="Water Records",
    #     relation="subject_water_record_rel",
    # )
    record_ids = fields.One2many(
        comodel_name="ar.record",
        string="Records",
        inverse_name="subject_id",
    )

    @api.depends('protocol_id')
    def get_animal_name(self):
        if self.protocol_id:
           self.animal_name = self.protocol_id.animal_name

    @api.depends('protocol_id')
    def get_study_id(self):
        if self.protocol_id:
           self.study_id = self.protocol_id.study_id

    def move_to_subject(self):
        subject_form = self.env.ref('animal_room.ar_subject_form_view', False)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ar.subject',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': subject_form.id,
        }

    def move_to_records(self, tree_name, category_name):
        view_id = self.env.ref('animal_room.view_subject_record_tree').id
        return {
            'name': tree_name,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'ar.record',
            'views': [(view_id, 'tree')],
            'domain': [('category_name', '=', category_name)],
            'context': {'default_subject_id': self.id},
        }

    def move_to_bodyweight(self):
        print("move_to_bodyweight")
        return self.move_to_records('Bodyweight Records', 'Bodyweight')

    def move_to_food(self):
        print("move_to_food")
        return self.move_to_records('Food Records', 'Food')

    def move_to_water(self):
        print("move_to_water")
        return self.move_to_records('Water Records', 'Water')
