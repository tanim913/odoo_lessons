from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class QualityControlWebsite(http.Controller):

    @http.route('/jobs/apply', type='http', auth='public', website=True)
    def job_application_form(self, **kw):
        """Render the job application form."""
        return request.render('quality_control.job_application_form_template', {})

    @http.route('/jobs/submit', type='http', auth='public', website=True, methods=['POST'])
    def job_application_submit(self, **post):
        """Handle the job application form submission."""
        import base64
        
        # Extract the uploaded file
        resume_file = post.get('resume')
        resume_base64 = False
        resume_name = False
        
        if resume_file:
            resume_base64 = base64.b64encode(resume_file.read())
            resume_name = resume_file.filename

        # Save to database (sudo because public user might not have access if not configured properly, though we gave them create access)
        application = request.env['quality.job.application'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'resume': resume_base64,
            'resume_name': resume_name,
        })
        
        values = {
            'name': application.name,
            'email': application.email,
        }
        return request.render('quality_control.job_application_success_template', values)

class PortalJobApplication(CustomerPortal):
    
    def _prepare_home_portal_values(self, counters):
        """Add job applications count to portal home."""
        values = super()._prepare_home_portal_values(counters)
        if 'job_count' in counters:
            job_count = request.env['quality.job.application'].search_count([])
            values['job_count'] = job_count
        return values

    @http.route(['/my/applications', '/my/applications/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_applications(self, page=1, **kwargs):
        """Render the list of applications for the portal user."""
        applications = request.env['quality.job.application'].search([])
        return request.render("quality_control.portal_my_applications", {'applications': applications})
