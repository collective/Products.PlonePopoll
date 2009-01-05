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
PlonePopollTool tool
"""

# $Id: PlonePopollTool.py 49714 2007-09-19 17:01:08Z glenfant $

import time, random
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from OFS import ObjectManager
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions as CMFCorePermissions
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from PlonePopollBackend import PlonePopollZODBBackend as BackendClass

from config import PlonePopoll_votePermission
from Products.PlonePopoll import logger

class PlonePopollTool(UniqueObject, ObjectManager.ObjectManager, SimpleItem):
    """
    PlonePopollTool tool
    """

    id = 'portal_popoll'
    meta_type = title = 'PlonePopoll Tool'
    security = ClassSecurityInfo()

    manage_options = (
        { 'label': 'Content',
         'action': 'manage_main',},
        { 'label': 'Migration',
          'action': 'manage_migration' },
        ) + SimpleItem.manage_options

    #
    #   ZMI methods
    #
    #security.declareProtected(ManagePortal, 'manage_migration' )
    manage_migration = PageTemplateFile('www/manage_migration', globals())

    def __init__(self, *args, **kw):
        super(PlonePopollTool, self).__init__(*args, **kw)
        back_end = BackendClass()
        self._setObject('PlonePopollBackend', back_end)
        return


    def listBackends(self):
        """
        listBackends(self, ) => return a list of available backends
        """
        # FIXME: seems to be useless
        pass


    def getBackend(self):
        """
        getBackend(self,) => return the backend
        """
        return self.PlonePopollBackend


    def getVoteUnicity(self, poll_id, create = 1):
        """
        getVoteUnicity(self, poll_id, create = 1) => string or int or None

        return a tag that allows PlonePopollTool to think that this vote isn't
        made twice for the same user.

        We first try to use the username as a tag. If it's not available or if
        the user is anonymous, we use a counter.

        - poll_id is the poll id (!), ie. a sitewide unique id identifying the poll.
          IT MUST NOT CHANGE DURING THE POLL'S LIFE.

        - create is an additional parameter set to 1 by default. If it is true,
          a new unicity token will be automatically generated. If it is false, this
          method returns the FORMER one if it exists, OR None if no token exists.
          This is convenient to check if a user has voted without consuming a
          ZODB transaction. => NOT USED
        """
        # Try to fetch the user name
        unicity = None
        mtool = getToolByName(self, 'portal_membership')

        try:
            if not mtool.isAnonymousUser():
                unicity = mtool.getAuthenticatedMember().getUserName()
        except:
            raise NameError, 'unicity' + unicity
            logger.error("Unable to find username %s", exc_info=True)
            pass

        # If we didn't find a valid user name, then we use a counter and store it
        # in a cookie
        logger.debug("Computing unicity")
        if not unicity:
            if self.REQUEST.has_key('AnonymousVoted%s' % (poll_id)):
                unicity = self.REQUEST['AnonymousVoted%s' % (poll_id)]
            elif create:
                unicity = int(time.time() * 10000000) + random.randint(0,99)
                expires = 'Wed, 19 Feb 2020 14:28:00 GMT'
                self.REQUEST.RESPONSE.setCookie(
                    'AnonymousVoted%s' % (poll_id,), str(unicity), path='/', expires=expires,
                    )

        # Add the poll id to the unicity factor
        logger.debug("bloub %s", unicity)
        if unicity:
            unicity = "%s%s" % (unicity, poll_id, )

        # Return unicity factor
        return unicity

    #                                                                           #
    #                           PlonePopoll configuration                       #
    #                                                                           #

    def setPortletConfiguration(self, **kwargs):
        """
        Configure PlonePopoll portlet
        """
        conf = getattr(self, 'portlet_configuration')
        for k, v in kwargs.items():
            conf[k] = v

    def getPortletConfiguration(self, key):
        """
        Get configuration of PlonePopoll portlet
        """
        conf = getattr(self, 'portlet_configuration')
        return conf.get(key)

    security.declareProtected(CMFCorePermissions.ManagePortal, 'manage_migrate')
    def manage_migrate(self, REQUEST=None):
        """Run Extensions.Migration.migrateToArchetypes.
        """
        from Products.PlonePopoll.Extensions import Migration
        out = Migration.migrateToArchetypes(self, REQUEST)
        return out

    security.declareProtected(CMFCorePermissions.View, 'canVote')
    def canVote(self, poll):
        """
            Check permission for voting
        """
        mtool = getToolByName(self, 'portal_membership')
        return mtool.checkPermission(PlonePopoll_votePermission, poll)


InitializeClass(PlonePopollTool)



#                                                                           #
#                           PlonePopollToolBackend management               #
#                                                                           #

def registerBackend(self, *args, **kw):
    """
    registerBackend(self, ...) => register a backend class into the system
    """
    pass        # $$$ TODO !
