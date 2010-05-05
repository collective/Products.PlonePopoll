###########
PlonePopoll
###########

By Ingeniweb_.

--------------------------

.. contents:: **Table of contents**

--------------------------

About PlonePopoll
#################

This is a Poll tool for Plone.

Requirements
############

* Plone 3.0

Instalation
###########

Add Products.PlonePopoll in your buildout.cfg eggs list.

Use the portal_quickinstaller of your Plone site.

Contributors and others can add polls.

Managers can add and configure PoPoll portlets using the new Plone 3
portlets managers.

Users of older PlonePopoll versions will notice that the (now useless)
configuration panel has disappeared.

Copyright and license
#####################

Copyright (c) 2005-2009 Ingeniweb_ SAS

This software is subject to the provisions of the GNU General Public License,
Version 2.0 (GPL).  A copy of the GPL should accompany this distribution.
THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
FOR A PARTICULAR PURPOSE

See the `LICENSE` file that comes with this product.

Architecture
############

A poll can be in one and only one of those states:

* enabled
* disabled

Results can be in one and only one of those states:

* visible
* not visible

Poll can have multiple choice activated, determining how many choice a
user can do.


Note
####

Within Plone, it's possible to vote for a poll only if it is enabled
AND published.

Results are displayed only when the *Results Visibility* is set to
visible.


Migration
#########

If you migrate from an oooooold PlonePopoll version (1.x) that's not
Archetypes based, create an external method in your Plone site:

* Id: migrate_popoll
* Title: (whatever)
* Module: PlonePopoll.Migration
* Function: migrateToArchetypes

Then click the "Test" tab of this external method.


Downloads
#########

You may find newer stable versions of PlonePopoll and pointers to
related informations (tracker, doc, ...) from
http://plone.org/products/plonepopoll


Subversion repository
#####################

Stay in tune with the freshest (maybe unstable) versions or
participate to the PlonePopoll evolutions:

https://svn.plone.org/svn/collective/PlonePopoll


API Documentation
#################

http://ingeniweb.sourceforge.net/Products/PlonePopoll/api/PlonePopoll.html


More information about PlonePopoll
##################################

http://ingeniweb.sourceforge.net/Products/PlonePopoll


Support and feedback
####################

Please read all the documentation that comes with this product before
asking for support, unless you might get a RTFM reply ;)

Note that we do not support the SQL storage mode anymore. The SQL
storage mode is an old third party contribution that has not been
maintained for a long time. If you want it back, volunteers are
welcome ;)

Localisation issues - other than french and english - should be
reported to the relevant translators (see Credits_ below).

Report bugs using the tracker (the `Tracker` link from
http://plone.org/products/plonepopoll). Please provide in your bug
report:

* Your configuration (Operating system+Zope+Plone+Products/versions).
* The full traceback if available.
* One or more scenario that triggers the bug.

Note that we do not support bug reports on Subversion trunk or
branches checkouts, unless

`Mail to Ingeniweb support <mailto:support@ingeniweb.com>`_ in English or
French to ask for specific support.

`Donations are welcome for new features requests
<http://sourceforge.net/project/project_donations.php?group_id=74634>`_


Credits
#######

Developers
==========

* Main developer: `Christophe "big" Bosse <mailto:christophe.bosse@ingeniweb.com>`_
* Plone 3 support: `Gilles Lenfant <mailto:gilles.lenfant@ingeniweb.com>`_
* Plone 4 support: `JC Brand <mailto:brand@syslab.com>`_

Translations (other than French and English)
============================================

* Bulgarian (bg): `Plamen Petkov <plamendp@bgstore.com>`_
* Czeck (cs): `Radim Novotny <novotny.radim@gmail.com>`_
* Danish (da): `Sven Burkert <svenburkert@web.de>`_
* German (de): `Sven Burkert <svenburkert@web.de>`_
* Greek (el): `Menelaos Maglis <mmaglis@metacom.gr>`_
* Esperanto (eo): `Jan Ulrich Hasecke <jan.ulrich@hasecke.com>`_
* Spanish (es): `Mikel Larreategi <mlarreategi@codesyntax.com>`_
* Basque (eu): `Mikel Larreategi <mlarreategi@codesyntax.com>`_, `Ales Zabala Alava <shagi@gisa-elkartea.org>`_
* Italian (it): `Massimiliano <baldomax@hotmail.com>`_
* Dutsch (nl): `Michael Reitsma <michael@reitsma.biz>`_
* Polish (pl): `Maciej Dziergwa <developing@extreme-is.com>`_
* Portugese-Brazilian (pt-br): `Luis Flavio Rocha <lflrocha@gmail.com>`_
* Russian (ru): `Andrey Fedoseev <andrey.fedoseev@gmail.com>`_
* Slovenian (sl): `Matjaz Jeran <matjaz.jeran@amis.net>`_
* Swedish (sv): `Jens Hjalmarsson <jens@hjalmarsson.se>`_
* Catalan (ca): `Pilar Marinas <pilar.marinas@upcnet.es>`_

--------------------------

#######
CHANGES
#######

Considered future features
##########################

New types of polls may be interesting (Idea from
http://www.apwiz.com/flexivote.htm):

* open poll lets you see results before voting
* in a blind vote you must vote first, but can see all details
* In private poll you see results but not how people voted
* In a secret vote only the owner can see results and voting pattern.

To do
#####

* Test SQL back-end (find volunteers, we don't want to support this in
  the future).

* Cleanup and spread in appropriate external methods what's in
  Extensions/Install.py. We install with GenericSetup from now.

* Provide zconfig features to select and configure the votes back-end
  (see note about SQL back-end above)

* Use a Zope 3 view for the poll to speed up

* Should we keep migrations ? (useless for old AT based Popoll).

* Notify translators about new msgids.

* Why are the entries of the combo in portlet configuration untranslated when the code (browser/popoll.py)

.. sectnum::
.. _Ingeniweb: http://www.ingeniweb.com/
.. $Id: README.txt 77758 2008-12-17 16:36:28Z sneridagh $

