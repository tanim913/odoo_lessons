from odoo import api, fields, models

class QualityJobApplication(models.Model):
    _name = 'quality.job.application'
    _description = 'Quality Inspector Job Application'
    _order = 'create_date desc'

    name = fields.Char('Applicant Name', required=True)
    email = fields.Char('Email Address', required=True)
    phone = fields.Char('Phone Number')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')
    
    resume = fields.Binary('Resume', attachment=True)
    resume_name = fields.Char('Resume File Name')
    
    # We will use create_uid for portal access automatically since Odoo handles it for logged in users
