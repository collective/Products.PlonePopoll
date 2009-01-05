# -*- coding: utf-8 -*-
## PlonePopoll: A Plone poll tool
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
The Popoll portlet logic and services
"""
# $Id: popoll.py 77777 2008-12-17 22:38:08Z duane $

__docformat__ = 'restructuredtext'

from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.PlonePopoll import PopollMessageFactory as _


class IPopollPortlet(IPortletDataProvider):
    """Portlet configuration data model"""

    selection_mode = schema.Choice(
        title=_(u'label_plonepopoll_portlet_configuration'),
        description=_(u'help_plonepopoll_portlet_configuration'),
        vocabulary="popoll.portlet.pollselection"
        )


    number_of_polls = schema.Int(
        title=_(u'label_plonepopoll_portlet_configuration_number_of_polls'),
        description=_(u'help_plonepopoll_portlet_configuration_number_of_polls'),
        required=True,
        default=5
        )


class SourcesVocabulary(object):
    """Provides vocabulary to IPopollPortlet.selection_mode through ZCML"""

    implements(IVocabularyFactory)

    def __call__(self, context):

        context = getattr(context, 'context', context)
        portal_catalog = getToolByName(context, 'portal_catalog')

        # Basic options
        voc  = [
            SimpleTerm('hidden', title=_(u'label_portlet_configuration_hidden', default=u"Hidden")),
            SimpleTerm('newest', title=_(u'label_portlet_configuration_newest', default=u"Newest")),
            SimpleTerm('branch', title=_(u'label_portlet_configuration_branch', default=u"Branch")),
            SimpleTerm('subbranches', title=_(u'label_portlet_configuration_subbranches', default="Subbranches"))
            ]

        # Adding existing polls
        brains = portal_catalog.unrestrictedSearchResults(meta_type='PlonePopoll',
            allowedRolesAndUsers=['Anonymous'])
        for brain in brains: # Brains
            poll = brain.getObject()
            path = '/'.join(poll.getPhysicalPath())
            title = "%s (%s)" % (safe_unicode(brain.Title), safe_unicode(path))
            voc.append(SimpleTerm(poll.UID(), title=title))
        return SimpleVocabulary(voc)

SourcesVocabularyFactory = SourcesVocabulary()


class Assignment(base.Assignment):
    implements(IPopollPortlet)

    def __init__(self, selection_mode='hidden', number_of_polls=5):

        self.selection_mode = selection_mode
        self.number_of_polls = number_of_polls
        return

    @property
    def title(self):
        return _(u'heading_portlet_polls')


class Renderer(base.Renderer):
    """The class that builds the portlet"""

    # Note that we can't cache data cause some are per user

    _template = ViewPageTemplateFile('popoll.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.polls = self._polls()
        return

    def render(self):
        return xhtml_compress(self._template())

    def portal_url(self):
        utool = getToolByName(self.context, 'portal_url')
        return utool()

    def has_polls(self):
        return len(self.polls) > 0

    def has_more_polls(self):
        return len(self.polls) > 1

    def _polls(self):
        # Note that we can't cache poll data since some of them are user dependant
        context = aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        plone_tool = getToolByName(context, 'plone_utils')
        # I "love" the Plone 3 way to get the folderishness of a content :/
        #globals_view = getMultiAdapter((self.context, self.request), name='plone')
        #isStructuralFolder = globals_view.isStructuralFolder
        selection_mode = self.data.selection_mode
        number_of_polls = self.data.number_of_polls

        if selection_mode == 'hidden':
            results = []
        elif selection_mode == 'newest':
            results = portal_catalog.searchResults(
                meta_type='PlonePopoll',
                isEnabled=True,
                sort_on='Date',
                sort_order='reverse',
                sort_limit=number_of_polls)[:number_of_polls]

        elif selection_mode in ('branch', 'subbranches'):
            folder = context
            if not plone_tool.isStructuralFolder(context):
                folder = context.getParentNode()
            depth = (selection_mode == 'branch') and 1 or 1000
            results = portal_catalog.searchResults(
                meta_type='PlonePopoll',
                path={'query': '/'.join(folder.getPhysicalPath()),'depth': depth},
                isEnabled=True,
                sort_on='Date',
                sort_order='reverse',
                sort_limit=number_of_polls)[:number_of_polls]

        else:
            # A specific poll
            results = portal_catalog.searchResults(
                meta_type='PlonePopoll',
                UID=selection_mode)
        if results:
            return [pollFeatures(r.getObject()) for r in results]
        return []

def pollFeatures(poll):
    """Poll features for portlet layout"""

    sm = getSecurityManager()
    poll_url = poll.absolute_url()
    choices_count = poll.getNumber_of_choices()
    rval = {
        'url': poll_url,
        'choices_count': choices_count,
        'can_vote': poll.canVote(),
        'title': poll.Title(),
        'question': poll.getQuestion(),
        'form_action': '%s/vote' % poll_url,
        'form_name': 'results-%s' % poll.getId(),
        'results': poll.getResults(),
        'input_widget': choices_count > 1 and 'checkbox' or 'radio',
        'show_results': poll.isVisible() and poll.getShowCurrentResults(),
        'is_visible' : poll.isVisible(),
        'votes_count': poll.getVotesCount()
        }
    # TODO: on reprend au dessus
    return rval



class AddForm(base.AddForm):
    """Add form for our portlet"""

    form_fields = form.Fields(IPopollPortlet)

    label = _(u"add_portlet")
    description = _(u"desc_portlet")

    def create(self, data):
        return Assignment(
            selection_mode=data.get('selection_mode', 'hidden'),
            number_of_polls=data.get('number_of_polls', 5)
            )


class EditForm(base.EditForm):
    """Edit form for our portlet"""

    form_fields = form.Fields(IPopollPortlet)
    label = _(u"edit_portlet")
    description = _(u"desc_portlet")

