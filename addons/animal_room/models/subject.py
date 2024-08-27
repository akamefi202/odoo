from odoo import models, fields, api


class Subject(models.Model):
    _name = 'ar.subject'
    _description = 'ar_subject'

    uai = fields.Char(string="Unique Animal ID", readonly=True)
    sex = fields.Char(string="Sex", required=True, readonly=True)
    study_id = fields.Many2one(
        comodel_name='study.study',
        string="Associate Study",
        required=True,
        readonly=True,
    )
    animal_name = fields.Char(string="Animal Name", compute="get_animal_name", required=True, readonly=True)
    protocol_id = fields.Many2one(comodel_name="ar.protocol", string="Protocol", required=True)
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

    # selected bool value for subject selection dialog of clinical pathology module
    selected = fields.Boolean(default=False)

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

    def move_to_bodyweight(self):
        print("move_to_bodyweight")
        view_id = self.env.ref('animal_room.view_subject_record_tree').id
        return {
            'name': 'Bodyweight Records',
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'ar.record',
            'views': [(view_id, 'tree')],
            'domain': [('category_name', '=', 'Bodyweight')],
            'context': {'default_subject_id': self.id},
        }

    def move_to_food(self):
        print("move_to_food")
        view_id = self.env.ref('animal_room.view_subject_record_tree').id
        return {
            'name': 'Food Records',
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'ar.record',
            'res_id': self.id,
            'views': [(view_id, 'tree')],
            'domain': [('id', 'in', self.record_ids.ids), ('category_name', '=', 'Food')],
            'context': {'default_subject_id': self.id},
        }

    def move_to_water(self):
        print("move_to_water")
        view_id = self.env.ref('animal_room.view_subject_record_tree').id
        return {
            'name': 'Water Records',
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'res_model': 'ar.record',
            'views': [(view_id, 'tree')],
            #'domain': [('id', 'in', self.water_record_ids.ids)],
            'domain': [('id', 'in', self.record_ids.ids), ('category_name', '=', 'Water')],
            'context': {'default_subject_id': self.id},
        }
