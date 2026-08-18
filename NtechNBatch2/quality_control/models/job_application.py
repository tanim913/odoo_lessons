from odoo import api, fields, models


class QualityJobApplication(models.Model):
    _name = 'quality.job.application'
    _description = 'Quality Inspector Job Application'
    _order = 'create_date desc'

    name = fields.Char('Applicant Name', required=True)
    email = fields.Char('Email Address', required=True)
    phone = fields.Char('Phone Number')
    position = fields.Selection([
        ('qa_inspector', 'QA Inspector'),
        ('qa_engineer', 'QA Engineer'),
        ('qa_lead', 'QA Lead'),
    ], string='Position', default='qa_inspector')
    cover_letter = fields.Text('Cover Letter')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    resume = fields.Binary('Resume', attachment=True)
    resume_name = fields.Char('Resume File Name')

    # Link to partner for portal access filtering
    # When a logged-in user submits, we store their partner_id
    # This is more reliable than create_uid for portal filtering
    partner_id = fields.Many2one('res.partner', string='Applicant Partner', index=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-assign partner_id from logged-in user during creation."""
        for vals in vals_list:
            if not vals.get('partner_id') and not self.env.user._is_public():
                vals['partner_id'] = self.env.user.partner_id.id
        return super().create(vals_list)
