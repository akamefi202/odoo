import logging
from typing import Dict, List

from odoo import api, models, fields


class Study(models.Model):
    _name = "study.study"
    _description = "study_study"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string="Study Title", required=True)
    name = fields.Char(string="Study Name", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Datetime.now(), required=True)
    end_date = fields.Date(string="End Date", required=True)
    prestudy_days = fields.Integer(string="Pre-study Days", required=True)
    recovery_days = fields.Integer(string="Recovery Days", required=True)
    animal_number_total = fields.Integer(string="Total Number of Animals", required=True)
    animal_number_per_cage = fields.Integer(string="Number of Animals Per Cage", required=True)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("approved", "Approved"),
            ("closed", "Closed"),
        ],
        string="Status",
        default="draft",
        required=True,
    )
    archived = fields.Boolean(string="Archived", default=False)
    director_id = fields.Many2one(
        comodel_name='res.users',
        string="Director",
        index=True,
        required=True)
    article_id = fields.Many2one(
        comodel_name='study.article',
        string="Article",
        required=True)
    animal_id = fields.Many2one(
        comodel_name='study.animal',
        string="Animal",
        required=True)
    group_ids = fields.One2many(
        comodel_name="study.group",
        inverse_name="study_id",
        string="Study Groups",
    )
    comment = fields.Text(string="Comment", required=False, default="")

    @api.depends('name')
    def _compute_user_role(self):
        print(self.user.role)

    @api.depends("start_date")
    def _onchange_start_date(self):
        print("_onchange_start_date")
        self.env['study.record'].create({
            'user_id': self.env.user.id,
            'study_id': self.id,
            'text': "\'Study Title\' field is updated by {0}".format(self.env.user.name),
        })

    def action_create(self):
        print("Create Button")
        self.status = "draft"

    def action_approve(self):
        print("Approve Button")
        self.status = "approved"

    def action_close(self):
        print("Close Button")
        self.status = "closed"

    def action_archive(self):
        print("Archive Button")
        self.archived = True

    def action_unarchive(self):
        print("Archive Button")
        self.archived = False

    def action_edit(self):
        print("Edit Button")

    def action_delete(self):
        print("Edit Button")