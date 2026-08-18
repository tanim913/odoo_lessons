import base64

from odoo import http
from odoo.http import request

from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class QualityControlWebsite(http.Controller):
    """Public website controllers for quality_control module."""

    @http.route('/quality/checks', type='http', auth='public', website=True)
    def quality_checks_page(self, **kw):
        """Public page showing quality checks — demonstrates qcontext dict passing."""
        checks = request.env['quality.check'].sudo().search([], limit=20)
        # qcontext: a Python dict passed to the QWeb template
        # Every key becomes a variable usable inside the template
        qcontext = {
            'checks': checks,
            'page_title': 'Quality Checks Overview',
            'company_name': request.env.company.name,
        }
        return request.render('quality_control.quality_checks_page_template', qcontext)

    @http.route('/jobs/apply', type='http', auth='public', website=True)
    def job_application_form(self, **kw):
        """Render the job application form with position choices via qcontext."""
        positions = [
            ('qa_inspector', 'QA Inspector'),
            ('qa_engineer', 'QA Engineer'),
            ('qa_lead', 'QA Lead'),
        ]
        values = {
            'positions': positions,
        }
        return request.render('quality_control.job_application_form_template', values)

    @http.route('/jobs/submit', type='http', auth='public', website=True, methods=['POST'])
    def job_application_submit(self, **post):
        """Handle the job application form submission."""
        # Extract the uploaded file
        resume_file = post.get('resume')
        resume_base64 = False
        resume_name = False

        if resume_file:
            resume_base64 = base64.b64encode(resume_file.read())
            resume_name = resume_file.filename

        # Build creation vals
        vals = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'position': post.get('position', 'qa_inspector'),
            'cover_letter': post.get('cover_letter'),
            'resume': resume_base64,
            'resume_name': resume_name,
        }

        # If user is logged in (portal or internal), link their partner
        if not request.env.user._is_public():
            vals['partner_id'] = request.env.user.partner_id.id

        # sudo() required: public users have no write access to our model
        application = request.env['quality.job.application'].sudo().create(vals)

        return request.render('quality_control.job_application_success_template', {
            'name': application.name,
            'email': application.email,
            'position': dict(application._fields['position'].selection).get(application.position),
        })


class PortalJobApplication(CustomerPortal):
    """Portal controllers — following the same pattern as sale module."""

    def _prepare_home_portal_values(self, counters):
        """Add job applications count to portal home dashboard."""
        values = super()._prepare_home_portal_values(counters)
        if 'job_application_count' in counters:
            JobApp = request.env['quality.job.application']
            values['job_application_count'] = (
                JobApp.search_count([])
                if JobApp.has_access('read')
                else 0
            )
        return values

    @http.route(
        ['/my/applications', '/my/applications/page/<int:page>'],
        type='http', auth='user', website=True,
    )
    def portal_my_applications(self, page=1, sortby=None, **kwargs):
        """Portal list of job applications for the logged-in user.

        Portal users see only their own records (filtered by ir.rule).
        Internal users see all records.
        """
        JobApp = request.env['quality.job.application']
        values = self._prepare_portal_layout_values()

        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'create_date desc'},
            'name': {'label': 'Name', 'order': 'name asc'},
            'state': {'label': 'Status', 'order': 'state asc'},
        }
        if not sortby:
            sortby = 'date'

        sort_order = searchbar_sortings[sortby]['order']
        # The ir.rule automatically filters: portal sees own, internal sees all
        application_count = JobApp.search_count([])

        pager = portal_pager(
            url='/my/applications',
            total=application_count,
            page=page,
            step=self._items_per_page,
        )

        applications = JobApp.search(
            [], order=sort_order,
            limit=self._items_per_page,
            offset=pager['offset'],
        )

        values.update({
            'applications': applications,
            'page_name': 'my_applications',
            'pager': pager,
            'default_url': '/my/applications',
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
        })
        return request.render('quality_control.portal_my_applications', values)

    @http.route(['/my/applications/<int:application_id>'], type='http', auth="user", website=True)
    def portal_my_application_detail(self, application_id, **kw):
        """Detail view for a single job application."""
        try:
            # _document_check_access checks ir.rules
            application_sudo = self._document_check_access('quality.job.application', application_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._prepare_portal_layout_values()
        values.update({
            'application': application_sudo,
            'page_name': 'my_applications',
        })
        return request.render('quality_control.portal_my_application_detail', values)
