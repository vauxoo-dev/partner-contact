# -*- coding: utf-8 -*-
# © 2016 Vauxoo (http://www.vauxoo.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Nhomar Hernandez <nhomar@vauxoo.com>
from openerp import api, models
from openerp.addons.base.ir.ir_qweb import QWebException


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def pick_view(self):
        """First look into the countries partner if not the it goes to the
        company value (which will be the default one) an then pick the first
        one found.

        If the view_format_id is passed as part of the context keys then it will
        return the wired value.

        :return ir.ui.view: Picked view
        """

        ctx = dict(self._context)
        self.ensure_one()
        # If you use pass wired a view ID by context then it will have the
        # highest priority.
        view_format_id = ctx.get('view_format_id')
        if view_format_id is not None:
            return self.env.ref(view_format_id)
        # Higher priority "Country in Partner Address"
        if self.country_id and self.country_id.address_format_id:
            return self.country_id.address_format_id
        # You can force one address into the company if none into the Country.
        users = self.env['res.users']
        company = users.browse(self._uid).company_id
        company_view = company.address_format_id
        if company_view:
            return company_view
        # If Nothing is predefined properly returns a default one.
        return self.env.ref('partner_address_format.default')

    @api.cr_uid_ids_context
    def get_address_from_template(self, cr, uid, ids, context=None):
        """Generate the html view already rendered to be used either into a
        field or directly from a method.

        :param context: view_format_id key ensure use that specific view.
        :return str: Address in html format.
        """
        context = context is None and {} or context
        view = self.pick_view(cr, uid, ids, context=context)
        val = {'partner': self.browse(cr, uid, ids[0], context=context), }
        try:
            # Catch any error in declaration of the view, if the user make an
            # error it will help in the debugging process.
            view_obj = self.pool['ir.ui.view']
            html = view_obj.render(cr, uid, view.id, val, context=context)
        except QWebException as exc:
            # For some reason the Exception from Qweb is not returning an
            # standard exception that's why you see the the repr
            return '{err} on view {view}'.format(err=repr(exc),
                                                 view=view and view.name or '')
        return html
