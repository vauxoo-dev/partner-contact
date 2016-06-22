# -*- coding: utf-8 -*-
# © 2016 Vauxoo (http://www.vauxoo.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Nhomar Hernandez <nhomar@vauxoo.com>
from openerp.tests.common import TransactionCase


class TestRender(TransactionCase):

    def setUp(self):
        super(TestRender, self).setUp()
        # Agrolait: To tests company addresses
        self.contact_use_parent = self.env.ref('base.res_partner_2')
        # Agrolait,
        # Thomas Passot To test a contact with a company.
        self.company_no_parent = self.env.ref('base.res_partner_address_3')
        # Demo portal User: To test a contact without a company as the portal
        # users ones.
        self.contact_no_company = self.env.ref('portal.partner_demo_portal')
        self.mexico = self.env.ref('base.mx')
        self.main_company = self.env.ref('base.main_company')
        self.view_on_company = self.env.ref('partner_address_format.company_format')  # noqa
        self.view_on_mx = self.env.ref('partner_address_format.partner_address_es_MX')  # noqa
        self.view_wired = self.env.ref('partner_address_format.short_format')
        self.view_default = self.env.ref('partner_address_format.default')
        self.templates = [
            'partner_address_format.partner_address_es_MX',
            'partner_address_format.default',
            'partner_address_format.partner_address_long_format',
            'partner_address_format.partner_address_es_MX',
            'partner_address_format.company_format',
            'partner_address_format.short_format',
        ]

    def test_001_pick_view_contact_use_parent(self):
        """Possibles algorithms to get the view country."""
        # set the partner with a known country with a known template
        self.contact_use_parent.country_id = self.mexico
        self.assertEqual(self.view_on_mx, self.contact_use_parent.pick_view(),
                         'Partner has a country with template set')

    def test_002_pick_view_contact_use_parent_no_country(self):
        """Expecting the template from the company ."""
        self.contact_use_parent.country_id = False
        view = self.contact_use_parent.pick_view()
        self.assertEqual(self.view_on_company, view,
                         'Returns "%s" instead' % view.name)

    def test_003_pick_view_blank_contact(self):
        """Nothing apply then validate the default is coming then"""
        blank_contact = self.env['res.partner'].create({
            'name': 'Blank named contact',
            'country_id': False,
        })
        view = blank_contact.pick_view()
        self.assertEqual(self.view_on_company, view,
                         'Returns: "%s" instead' % view.name)

    def test_004_pick_view_wired(self):
        """Forcing an specific view by context"""
        self.contact_use_parent.country_id = self.mexico
        ctx = {
            'view_format_id': 'partner_address_format.short_format'
        }
        view = self.contact_use_parent.with_context(ctx).pick_view()
        self.assertEqual(self.view_wired,
                         view,
                         'Returns:  %s' % view.name)

    def test_005_pick_view_default(self):
        """Forcing the default view if nothing properly configured"""
        self.contact_use_parent.country_id.address_format_id = False
        self.contact_use_parent.country_id = False
        self.main_company.address_format_id = False
        view = self.contact_use_parent.pick_view()
        self.assertEqual(self.view_default, view,
                         'Expecting the default view')

    def test_010_rendering_ok(self):
        """Rendering properly a template"""
        self.contact_use_parent.country_id = self.mexico
        view = self.contact_use_parent.get_address_from_template()
        self.assertIn('Mexico', view,
                      'Getting the rendering of a template fails.')

    def test_011_rendering_not_ok(self):
        """Rendering properly a broken template"""
        ctx = {'view_format_id': 'partner_address_format.demo_broken_format'}
        html = self.contact_use_parent.with_context(ctx).get_address_from_template()  # noqa
        self.assertIn('broken_element',
                      html,
                      'Element broken returns an unexpected output')

    def by_template_id(self, xml_id):
        """Assuming all properly configured, check the templates are working

        This set of tests are supposed to be called in every module that create
        a new template for address in order to test the template itself.
        In this case  we will be testing the template for the address added in
        this module with all known cases where the partner can be set.

        Remember, we can have logic inside the template to render it this
        method is to generalize the test It is more or less a framework of
        tests with the minimal required type of partners to be rendered."""
        ctx = {
            'view_format_id': xml_id
        }
        # Normal Contact which use a parent address from the company
        html = self.contact_use_parent.with_context(
            ctx).get_address_from_template()
        self.assertNotIn('QWebException', html,
                         'Template: %s  .' % xml_id)
        html = self.contact_no_company.with_context(
            ctx).get_address_from_template()
        self.assertNotIn('QWebException', html,
                         'Template: %s  .' % xml_id)
        html = self.company_no_parent.with_context(
            ctx).get_address_from_template()
        self.assertNotIn('QWebException', html,
                         'Template: %s  .' % xml_id)

    def test_020_address_templates(self):
        """Testing all templates on this module."""
        [self.by_template_id(template) for template in self.templates]
