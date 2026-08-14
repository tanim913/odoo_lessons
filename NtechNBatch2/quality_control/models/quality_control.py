# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

RESULT = [
    ("pass", "Pass"),
    ("fail", "Fail"),
]

class QualityCheck(models.Model):
    _name = "quality.check"
    _description = "Quality Control Check"
    _rec_name = "name"

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Reference Name must be unique!')
    ]

    # ==========================================
    # FIELD DEFINITIONS
    # ==========================================
    name = fields.Char(
        string="Reference",
        required=False,
        copy=False,
        readonly=False,
        default="New",
    )
    inspector_id = fields.Many2one("res.users", "Main Checker", required="True")
    quantity_lines = fields.One2many("quality.check.line", "line_id", string="Product Lines")
    additional_inspector_ids = fields.Many2many(
        comodel_name="res.users",
        string="Additional Inspectors",
    )
    check_date = fields.Date(
        string="Check Date",
        default=fields.Date.today,
    )
    remarks = fields.Text(
        string="Remarks",
    )
    result = fields.Selection(
        selection=RESULT,
        string="Result",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("hod", "HOD"),
            ("md", "MD"),
            ("approved", "Approved"),
            ("confirmed", "Confirmed"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    # quantity_lines = fields.One2many('quality.check.line', 'line_id','Product Line')
    #
    # # ==========================================
    # # ORM OVERRIDES
    # # # ==========================================
    # # @api.model
    # # def create(self, vals_list):
    # #     """Generates sequence reference number on creation."""
    # #     for vals in vals_list:
    # #         if vals.get("name", "New") == "New":
    # #             seq_code = "quality.check.code"
    # #             vals["name"] = self.env["ir.sequence"].next_by_code(seq_code) or "New"
    # #     return super(QualityCheck, self).create(vals_list)

    # # ==========================================
    # # BUSINESS ACTIONS
    # # ==========================================
    report_note = fields.Html("Report Notes", help="Notes to show on the quality check report.")

    @api.constrains('check_date')
    def _check_date(self):
        for record in self:
            if record.check_date > fields.Date.today():
                raise ValidationError("Check date cannot be in the future.")

    def action_confirm(self):
        """Moves the state to confirmed."""
        for record in self:
            record.state = "confirmed"
    
    def action_done(self):
        """Validates result and sets state to done."""
        for record in self:
            if not record.result:
                raise ValidationError("Please select Pass or Fail before completion.")
            record.state = "done"