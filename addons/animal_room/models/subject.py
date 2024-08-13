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
        readonly=True)
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

    filter_category_type = fields.Char(default="Bodyweight")
    record_ids = fields.One2many(
        comodel_name="ar.record",
        string="Records",
        inverse_name="subject_id",
        domain=[('category_name', '=', filter_category_type)]
    )
    filtered_record_ids = fields.Many2many(
        comodel_name="ar.record",
        string="Filtered Records",
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

    def filter_records(self):
        records = self.env['ar.record'].search([
            ("subject_id", "=", self.id),
            ("category_name", "=", self.filter_category_type)]
        )
        self.filtered_record_ids = records
        #self.record_ids.determine_domain("category_name", "=", self.filter_category_type)

    def move_to_bodyweight(self):
        print("move_to_bodyweight")
        self.filter_category_type = "Bodyweight"
        self.filter_records()

    def move_to_food(self):
        print("move_to_food")
        self.filter_category_type = "Food"
        self.filter_records()

    def move_to_water(self):
        print("move_to_water")
        self.filter_category_type = "Water"
        self.filter_records()
