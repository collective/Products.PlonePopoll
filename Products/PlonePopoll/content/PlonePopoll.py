# -*- coding: utf-8 -*-
## PlonePopoll: A Plone poll tool
## Copyright (C)2005-2007 Ingeniweb

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
PlonePopoll main class
"""
# $Id: PlonePopoll.py 73952 2008-10-18 23:41:51Z ruda_porto $

from Products.PlonePopoll import logger
from AccessControl import ClassSecurityInfo

# CMF imports

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import make_uuid

from Products.ATContentTypes import atct
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PlonePopoll.config import PROJECTNAME
from Products.PlonePopoll.content.schemata import PollSchema
from Products.PlonePopoll.config import *
from Products.PlonePopoll import PopollMessageFactory as _

finalizeATCTSchema(PollSchema)


class PlonePopoll(atct.ATCTContent):
    """PlonePopoll class"""

    id             = 'PlonePopoll'

    _at_rename_after_creation = True
    schema = PollSchema

    _check_multi      = 1
    text = ""    # Default text

    # Standard security settings
    security = ClassSecurityInfo()
    security.declareObjectProtected(permissions.View)            # $$$ Is this clever ? Isn't it better to make the object private ?
                                                                        # This method makes all class properties & methods protected by View by default

    # Init method
    security.declarePrivate('__init__')
    def __init__(self, id):
        """__init__(self, id)"""
        #PlonePopoll.inheritedAttribute('__init__')(self)
        super(PlonePopoll, self).__init__(id)
        self.id = id
        self.uid = make_uuid(id)


    security.declarePrivate('_post_init')
    def _post_init(self):
        """
        _post_init(self) => Post-init method (that is, method that is called AFTER the class has been set into the ZODB)
        """
        self.indexObject()

    security.declareProtected(permissions.View, 'Description')
    def Description(self):
        "Returns the description of the poll, which is in fact the question"
        return self.getQuestion()

    security.declareProtected(permissions.View, 'getVoteId')
    def getVoteId(self):
        """ return unique vote id """
        if hasattr(self, 'uid'):
            return self.uid
        else:
            return self.getId()

    security.declareProtected(PlonePopoll_editPermission, "setPollOptions")
    def setPollOptions(self, question = '', choices = [], choices_number = 1, check_multi = 1):
        """
        setPollOptions(self, question = '', choices = [], choices_number = 1, check_multi = 0)
        - set fields question, choices and max number of choices
        """
        self.getField('question').set(self, question)
        self.getField('number_of_choices').set(self, choices_number)
        self._check_multi = check_multi
        if choices:
            _choices = []
            for c in choices:   # We ensure that choices is a list
                _choices.append(c)
            self.getField('choices').set(self, _choices)  # Ensure persistancy


    security.declareProtected(PlonePopoll_votePermission, 'getPollNumber')
    def getPollNumber(self):
        """ compatibility layer """
        # FIXME: deprecated ? (kill this method ?)
        return self.getNumber_of_choices()

    security.declareProtected(PlonePopoll_votePermission, 'vote')
    def vote(self, choices=[], clear=False, redirect=True, redirect_url=None):
        """
        vote(self, choices = [], clear = False )
        - calls the backend to register votes
        - Include all the necessary code to pseudo-guarantee the unicity of the vote.
        """
        if not self.isEnabled():
            raise RuntimeError, "This poll is not active."
        if self.hasVoted():
            self.removeUserVote()

        request = self.REQUEST
        response = request.RESPONSE

        checkedCount = len(choices)
        max_votes = int(self.getNumber_of_choices())
        if clear:
            self.clearResults()
            msgstr = "Poll results have been cleared."
            msgid = "results_cleared"

        else:
            if checkedCount > max_votes and self._check_multi:
                msgstr = "You have made ${checked} choices. The maximum authorized is ${max}."
                msgid = 'message_check_count'

            else:
                portal_popoll = getToolByName(self, 'portal_popoll')
                # Ensure unicity of the vote
                unicity = portal_popoll.getVoteUnicity(self.getVoteId(), create=1)
                for choice in choices:
                    # Check that choice is valid
                    if int(choice) >= len(self.choices) or int(choice) < 0:
                        raise ValueError, "Invalid choice"

                    # Call the method in the backend to store the vote
                    portal_popoll.getBackend().vote(self.getVoteId(), int(choice), unicity)
                msgstr = "Vote has been saved."
                msgid = "vote_saved"

        message = _(unicode(msgid), default=unicode(msgstr), mapping={'checked': checkedCount, 'max': max_votes})
        plone_utils = getToolByName(self, 'plone_utils')
        plone_utils.addPortalMessage(message)
        if redirect:
            url = redirect_url or self.absolute_url()
            return response.redirect(url)


    security.declareProtected(PlonePopoll_votePermission, "hasVoted")
    def hasVoted(self):
        """
        hasVoted(self)
        - Return 1 if the user has already voted.
        This is based on the unicity token
        """
        unicity = getToolByName(self, 'portal_popoll').getVoteUnicity(self.getVoteId(), create = 0)
        if unicity:
            return getToolByName(self, 'portal_popoll').getBackend().hasAlreadyVoted(self.getVoteId(), unicity)
        return None

    ###
    ## Results management
    ###

    security.declareProtected(permissions.View, "getResults")
    def getResults(self, sort = 0):
        """
        getResults(self)
        -> return results as a TUPLE of tuples (id, count, percentage).

        percentage is 0 <= percentage <= 100

        The order is the same as for listChoiceIds if sort if false.
        If sort is true, results are sorted by score (best first)
        """
        res = getToolByName(self, 'portal_popoll').getBackend().getResults(self.getVoteId())
        ret = []
        votes_count = 0
        idx = 0
        for id in self.choices[:]:
            # If a choice has not been selected, it is not in res!
            if not res.has_key(idx):
                ret.append((id, 0))
            else:
                votes_count += res[idx]['count']
                ret.append((id, res[idx]['count']))
            idx += 1
        # Create a new tuple that includes the percentage as well
        result=[]
        for r in ret:
           try:
              percentage=float(r[1])/float(votes_count)*100.0
           except:
              percentage=0.0
           #result.append((r[0],r[1],int(percentage)))  ## We should not do the int(). Fixed (KA & MR) !
           result.append((r[0], r[1], percentage))

        if sort:
            result.sort(lambda x,y: cmp(y[1], x[1]))

        logger.debug("getResults for the popoll :%s", result)
        return tuple(result)

    security.declareProtected(permissions.View, "getVotesCount")
    def getVotesCount(self):
        """
            return total number of votes for this poll
        """
        ret = 0
        for id, count, percentage in self.getResults():
            ret += count

        return ret

    security.declareProtected(permissions.View, "getPersonVoteCount")
    def getPersonVoteCount(self):
        """ return number of votes for current user """
        return getToolByName(self, 'portal_popoll').getBackend().getPersonVoteCount(self.getVoteId())

    security.declareProtected(PlonePopoll_editPermission, "clearResults")
    def clearResults(self):
        """ Remove all votes for this poll """
        getToolByName(self, 'portal_popoll').getBackend().clearResults(self.getVoteId())


    security.declareProtected(permissions.View, "getUnicity")
    def getUnicity(self):
        """ """
        return getToolByName(self, 'portal_popoll').getVoteUnicity(self.getVoteId(), create=0)

    security.declareProtected(PlonePopoll_votePermission, "removeUserVote")
    def removeUserVote(self):
        """ """
        unicity = getToolByName(self, 'portal_popoll').getVoteUnicity(self.getVoteId(), create=0)
        getToolByName(self, 'portal_popoll').getBackend().removeUserVote(self.getVoteId(), unicity)


    #                                                                           #
    #                             CMF CATALOG SUPPORT                           #
    #                                                                           #

    security.declareProtected(permissions.View, 'SearchableText')
    def SearchableText(self):
        "Returns a concatination of all searchable text"
        # Should be overriden by portal objects
        return "%s %s %s" % (self.Title(), self.Description(), self.text)


    # helper methods
    security.declarePublic('canVote')
    def canVote(self):
        tool = getToolByName(self, 'portal_popoll')
        return (not self.hasVoted()
                and len(self.getChoices()) > 0
                and tool.canVote(self)
                and self.isEnabled())

    security.declarePublic('resultsVisible')
    def resultsVisible(self):
        mtool = getToolByName(self, 'portal_membership')
        return self.isVisible() or mtool.checkPermission(PlonePopoll_editPermission, self)


# AT register
registerType(PlonePopoll, PROJECTNAME)

def cloneHandler(ob, event):
    """ """
    ob.uid = make_uuid(id)
    return

