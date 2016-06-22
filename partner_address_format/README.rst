Partner Reusable Address Format
===============================

**Rationale**

We show the address of a partner in several reports (purchase, pickings, sales
online forms, etc.) then with this you will be allowed to set such address in
an standard way using some sort of business logic because it frequently depends
of it for example if you are in the country A and a customer in the country B
your address and yours can be in different format (even using more or less
fields) then using this module you will be able to configure per country such
formats, but if th country do not have such format, then it will look into the
company and you can use a generic way to show the address.

You can include (thanks to the Qweb Engine) all the complex logic it can
require to combine for example contacts with parent companies to generate
proper information to be shown in your reports.

Even if this module has some technical components it can be used with basic
Html-Qweb knowledge and you can manually set the templates into the database
with no problem avoiding expend in reports layers a lot of time debugging a
simple comma or a parenthesis to produce pretty and ordered printed address.

The hole point is that per country generally there is a proper manner of show
the address, then it does not make too much sense create 20 or 30 lines of
code xml per report, we can customize this elements per country and/or company
and use a pretty well know standard then.

An example of a very well explained set of address shown process is here:

https://es.wikipedia.org/wiki/Direcci%C3%B3n_postal

Install
=======

No necessary extra steps to install.

How to use
==========

Simply replace your address rendering in the report you need escaping the new
method available in the partner model called `get_address_from_template()`.

You can inherit the report and use an xpath or simply create your own report.

In order to format and render properly try to use labels and css elements from
twitter bootstrap or inline styles (if you want to show the field in an email
for example or nicer in a report).

.. code:: xml

    <div t-raw="partner.get_address_from_template()"/>

If you want use it into the Purchase report you can add this into your module
(or manually into the view using your administrative privileges) inheriting
properly the report template `purchase.purchase_order`.

.. code:: xml

    <xpath expr="//div[@class='placeholder']" position="replace">
        <div t-raw="partner.get_address_from_template()"/>
    </xpath>

Included Formats
================

1. Long en_US Format.
2. Long es_MX Format.
3. Short International format (used to show just contact info if company_id is
   present).

Hacking and Contributing
========================

If you need more pre loaded formats it is nice if you add the few views lines
into the file templates.xml and propose a proper PR.

Frequently you need render with special fields on partner, the recommendend way
is to depends of this module into the module which add the fields itself and
either inherit the templates here created and/or generate your own templates
there in order to propose to the end use a new template including your fields.

For support and new features call to Vauxoo or fill a proper issue.
