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

# $Id: Migration.py 57510 2008-01-23 13:34:01Z glenfant $

# CMF imports
from Products.CMFCore.utils import getToolByName

# Product imports
from Products.PlonePopoll.config import *

from copy import copy
from Persistence import PersistentMapping
from Acquisition import aq_base

def migrateToArchetypes(self, REQUEST=None):
    print """
    -------------------------------------------------
        Execute migration from old CMF PlonePopoll
        to the new archetypes one
    """
    nb_updated = 0
    #Check if it is needed to migrate to Archetypes
    pcatalog = getToolByName(self, 'portal_catalog')
    brains = pcatalog.searchResults(meta_type='PlonePopoll')
    for brain in brains:
        poll = brain.getObject()
        if hasattr(poll, '_question'):
            updateObject(poll)
            nb_updated = nb_updated + 1

    if REQUEST is not None:
        return REQUEST.RESPONSE.redirect(
            self.absolute_url() + \
            '/manage_main?manage_tabs_message=%s+polls+updated' % nb_updated,
        )

def updateObject(old_poll):
    attributes = {
        '_question' : 'question',
        '_choices' : 'choices',
        '_number_of_choices' : 'number_of_choices',

    }
    creation_date = old_poll.creation_date
    modification_date = old_poll.modification_date
    parent = old_poll.getParentNode()

    poll_id = old_poll.id
    parent.manage_delObjects(poll_id)
    parent.invokeFactory('PlonePopoll', poll_id)
    new_poll = getattr(parent, poll_id)
    new_poll.setTitle(old_poll.title)
    if hasattr(aq_base(old_poll), 'getWrappedOwner'):
        new_poll.changeOwnership(old_poll.getWrappedOwner())
    else:
        new_poll.changeOwnership(old_poll.getOwner(info = 1))
    new_poll.creation_date = creation_date
    new_poll.modification_date = modification_date
    new_poll.setContentType(old_poll.content_type)
    new_poll.setSubject(old_poll.subject)
    new_poll.setContributors(old_poll.contributors)
    new_poll.setEffectiveDate(old_poll.effective_date)
    new_poll.setExpirationDate(old_poll.expiration_date)
    new_poll.setLanguage(old_poll.language)
    new_poll.allowDiscussion(old_poll.isDiscussable())
    if hasattr(old_poll, 'uid'):
        new_poll.uid = old_poll.uid
    wfh = getattr(old_poll, 'workflow_history', None)
    if wfh:
        wfh = copyPermMap(wfh)
        new_poll.workflow_history = wfh


    if hasattr(old_poll, '_poll_state'):
         new_poll.getField('enabled').set(
            new_poll,  getattr(old_poll, '_poll_state') == 'enabled'
         )
    if hasattr(old_poll, '_visibility'):
         new_poll.getField('visible').set(
            new_poll,  getattr(old_poll, '_visibility') == 'visible'
         )

    for attribute in attributes.keys():
        if hasattr(old_poll, attribute):
            new_poll.getField(attributes[attribute]).set(new_poll, getattr(old_poll, attribute))

def copyPermMap(old):
    """bullet proof copy
    """
    new = PersistentMapping()
    for k,v in old.items():
        nk = copy(k)
        nv = copy(v)
        new[k] = v
    return new

