import logging
from typing import Dict, List

from odoo import api, models, fields


class Study(models.Model):
    _name = "study.study"
    _description = "study_study"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string="Study Title", required=True, tracking=True)
    name = fields.Char(string="Study Name", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", default=fields.Datetime.now(), required=True, tracking=True)
    end_date = fields.Date(string="End Date", required=True, tracking=True)
    prestudy_days = fields.Integer(string="Pre-study Days", required=True, tracking=True)
    recovery_days = fields.Integer(string="Recovery Days", required=True, tracking=True)
    animal_number_total = fields.Integer(string="Total Number of Animals", required=True, tracking=True)
    animal_number_per_cage = fields.Integer(string="Number of Animals Per Cage", required=True, tracking=True)
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
    director = fields.Char(string="Director", required=True)
    article_name = fields.Selection(
        [
            ("article1", "Article 1"),
            ("article2", "Article 2"),
            ("article3", "Article 3"),
        ],
        string="Article",
        default="article1",
        required=True
    )
    animal_name = fields.Selection(
        [
            ("mouse", "Mouse"),
            ("cat", "Cat"),
            ("rabbit", "Rabbit"),
        ],
        string="Animal",
        default="mouse",
        required=True
    )
    comment = fields.Text(string="Comment", required=False, default="")
    #sd_user_id = fields.Many2one("res.users", string="SD Name", default=lambda self: self.env.user)
    #article_id = fields.Many2one("study.article", String="Article")
    #animal_id = fields.Many2one("study.animal", String="Animal")
    group_ids = fields.One2many(
        comodel_name="study.group",
        inverse_name="study_id",
        string="Study Groups",
    )

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