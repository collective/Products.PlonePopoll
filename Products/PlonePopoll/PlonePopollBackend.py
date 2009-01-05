# -*- coding: utf-8 -*-
## PlonePopoll: A Plone poll tool
## Copyright (C) 2005-2007 Ingeniweb

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
PlonePopoll product, votes back-ends
"""
# $Id: PlonePopollBackend.py 49713 2007-09-19 16:46:14Z glenfant $

from Globals import MessageDialog
from Globals import InitializeClass
from AccessControl.Role import RoleManager
import OFS
from Shared.DC.ZRDB.Results import Results

from Products.PlonePopoll import logger


class PlonePopollBackend(OFS.SimpleItem.SimpleItem):
    """
    PlonePopollBackend => A simple poll management interface
    """
    meta_type='PlonePopollBackend'
    id       ='PlonePopollBackend'
    title    ='A poll results data manager'


    def __init__(self):
        """
        __init__(self) -> initialization method
        """
        pass


    def _post_init(self):
        """
        _post_init(self) => called from manage_add method
        """
        pass


    #############################################################
    #                                                           #
    #                   Backend interface                       #
    #                                                           #
    #############################################################


    def vote(self, choice, unicity_factor, REQUEST = {}, **kw):
        """
        vote(self, choice, unicity_factor, REQUEST = {}, **kw) => place a vote on the acquired poll

        unicity_factor is a parameter that should be unique to each user. It's the way to keep track
        of multiple votes by a same person.
        """
        raise NotImplementedError, "Has to be redefined in subclasses"


    def getResults(self):
        """
        getResults(self) => return results as a dictionary:
        {
        id: {count: 0,},
        }
        """
        raise NotImplementedError, "Has to be redefined in subclasses"



#################################################################
#                                                               #
#                       ZODB BACKEND                            #
#                                                               #
#################################################################



class PlonePopollZODBBackend(PlonePopollBackend):
    """
    PlonePopollZODBBackend => A simple ZODB poll backend implementation
    """
    meta_type = "PlonePopollZODBBackend"


    def __init__(self):
        """ _results dictionary is made this way:
         {poll_id: { unicity_factor: vote,
                     unicity_factor: vote,
                       ...
                   },
          poll_id: { ...
                   },
          }
        """
        self._results = {}

    def removeUserVote(self, poll_id, unicity_factor):
        """
        remove the previous vote
        """
        self._results[poll_id][unicity_factor] = []
        logger.debug("removed user vote %s", self._results)
        logger.debug("User vote: %s", self._results[poll_id][unicity_factor])
        return

    def vote(self, poll_id, choice, unicity_factor, REQUEST = {}, **kw):
        """
        vote
        """
        # Record the vote in the _results dictionary
        if not self._results.has_key(poll_id):
            self._results[poll_id] = {}

        if not self._results.has_key(poll_id) or not self._results[poll_id].has_key(unicity_factor) :
            self._results[poll_id][unicity_factor] = []

        self._results[poll_id][unicity_factor].append(choice)

        self._results = self._results
        logger.debug("vote %s", self._results[poll_id])
        logger.debug("vote %s", self._results[poll_id][unicity_factor])
        logger.debug("vote %s", self._results)
        return

    def hasAlreadyVoted(self, poll_id, unicity_factor):
        """
        hasAlreadyVoted(self, unicity_factor) => return 1 if unicity_factor is already in the database
        """
        r = self._getResults()
        return r.get(poll_id, {}).has_key(unicity_factor)

    def _getResults(self):
        """
        _getResults(self) => private method for returning results
        """
        return self._results.copy()


    def getResults(self, poll_id):
        """
        getResults(self) -> dict {choice: {'count': count}}
        """
        ret = {}
        poll_results = self._results.get(poll_id, {}).items()
        for user, choices in poll_results :
            for choice in choices:
                if not ret.has_key(choice):
                    ret[choice] = {'count': 1}
                else:
                    ret[choice]['count'] += 1
        return ret


    def clearResults(self, poll_id):
        """
            clearResults(self) -> reset the _results dict of the poll_id  to {}
        """
        self._results[poll_id] = {}
        self._p_changed = 1


    def getPersonVoteCount(self, poll_id):
        """
        getPersonVoteCount(self, poll_id) -> int person count
        """
        ret = 0
        if not self._results.has_key(poll_id):
            return ret
        else:
            return len(self._results[poll_id])


class PlonePopollZSQLBackend(OFS.ObjectManager.ObjectManager, OFS.SimpleItem.Item, PlonePopollBackend):
    """
    PlonePopollZSQLBackend => A simple ZSQL poll backend implementation
    """
    _results = {}
    meta_type = "PlonePopollZSQLBackend"

    # Management interfaces
    manage_options=(
        OFS.ObjectManager.ObjectManager.manage_options
        + OFS.SimpleItem.Item.manage_options
        + RoleManager.manage_options
        )

    def safe_escape(self,param):
        return str(param).replace("\\", "\\\\").replace("'", "''").replace('"','""')

    def executeQuery(self,query):

        db = getattr(self, 'ZSQLDatabaseAdapter', None)
        if db:
            try:
                return db().query(query)
            except:
                raise "Cannot execute query: %s" % query
        else:
            return

    def SQLinit(self):
        query = "CREATE TABLE IF NOT EXISTS TM_POLL(POLL_Id VARCHAR(255), UNICITY_FACTOR VARCHAR(255), CHOICE_Id VARCHAR(255))"
        self.executeQuery(query)

    def SQLvote(self, poll_id, choice, unicity_factor):
        poll_id        = self.safe_escape(poll_id)
        unicity_factor = self.safe_escape(unicity_factor)
        choice         = self.safe_escape(choice)

        query = "INSERT INTO TM_POLL (POLL_Id, UNICITY_FACTOR,  CHOICE_Id) VALUES ('%s','%s','%s')" % (poll_id, unicity_factor, choice)
        self.executeQuery(query)

    def SQLgetResults(self,poll_id):
        poll_id        = self.safe_escape(poll_id)

        query = "SELECT CHOICE_Id, COUNT(UNICITY_FACTOR) FROM TM_POLL WHERE POLL_Id = '%s' GROUP BY CHOICE_Id" % poll_id
        res = self.executeQuery(query)
        return Results(res)

    def SQLhasVoted(self, poll_id, unicity_factor):
        poll_id        = self.safe_escape(poll_id)
        unicity_factor = self.safe_escape(unicity_factor)

        query = "SELECT COUNT(*) FROM TM_POLL WHERE POLL_Id = '%s' AND UNICITY_FACTOR = '%s'" % (poll_id,unicity_factor)
        res = self.executeQuery(query)
        return Results(res)

    def SQLclearResults(self, poll_id):
        poll_id        = self.safe_escape(poll_id)

        query = "DELETE FROM TM_POLL WHERE POLL_Id = '%s'" % poll_id
        self.executeQuery(query)

    def SQLpersonVoteCount(self, poll_id):
        poll_id        = self.safe_escape(poll_id)

        query = "SELECT COUNT(*) FROM TM_POLL WHERE POLL_Id = '%s'" % poll_id
        res = self.executeQuery(query)
        return Results(res)

    def SQLremoveUserVote(self, poll_id, unicity_factor):
        poll_id        = self.safe_escape(poll_id)
        unicity_factor = self.safe_escape(unicity_factor)

        query = "DELETE FROM TM_POLL WHERE POLL_Id = '%s' AND UNICITY_FACTOR = '%s'" % (poll_id, unicity_factor)
        self.executeQuery(query)


    def _post_init(self):
        self.SQLinit()


    def removeUserVote(self, poll_id, unicity_factor):
        """
        remove the previous vote
        """
        self.SQLremoveUserVote(poll_id = poll_id, unicity_factor = unicity_factor)


    def hasAlreadyVoted(self, poll_id, unicity_factor):
        """
        hasAlreadyVoted(self, unicity_factor) => return 1 if unicity_factor is already in the database
        """
        return len(self.SQLhasVoted(poll_id = poll_id, unicity_factor = unicity_factor))


    def clearResults(self, poll_id):
        """
            clearResults(self) -> reset the _results dict of the poll_id  to {}
        """
        self.SQLclearResults(poll_id = poll_id)


    def getPersonVoteCount(self, poll_id):
        """
        getPersonVoteCount(self, poll_id) -> int person count
        """
        ret = self.SQLpersonVoteCount(poll_id = poll_id)
        ret = ret.tuples()
        if len(ret):
            return int(ret[0][0])
        else:
            return 0


    def vote(self, poll_id, choice, unicity_factor, REQUEST = {}, **kw):
        """
        vote
        """
        self.SQLvote(poll_id = poll_id, choice = choice, unicity_factor = unicity_factor)


    def getResults(self, poll_id):
        """
        getResults(self) -> dict {choice: {'count': count}}
        """

        records = self.SQLgetResults(poll_id = poll_id)
        records = records.tuples()
        ret = {}
        for rec in records:
            ret[int(rec[0])] = {'count':int(rec[1])}

        return ret


# THIS IS TEMPORARY ! HAS TO BE REPLACED WITH AN INTERFACE THAT ALLOWS ONE
# TO CHOOSE HIS BACKEND $$$

def manage_addPlonePopollZODBBackend(self, REQUEST={}, **ignored):
    """ """
    f = PlonePopollZODBBackend()
    try:    self._setObject('PlonePopollBackend', f)
    except: return MessageDialog(
                   title  ='Item Exists',
                   message='This object already contains a PlonePopollBackend',
                   action ='%s/manage_main' % REQUEST['URL1'])
    self.PlonePopollBackend._post_init()
    if REQUEST.has_key('RESPONSE'):
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')


def manage_addPlonePopollZSQLBackend(self, REQUEST={}, **ignored):
    """ """
    f = PlonePopollZSQLBackend()
    try:    self._setObject('PlonePopollBackend', f)
    except: return MessageDialog(
                   title  ='Item Exists',
                   message='This object already contains a PlonePopollBackend',
                   action ='%s/manage_main' % REQUEST['URL1'])
    self.PlonePopollBackend._post_init()
    if REQUEST.has_key('RESPONSE'):
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')


InitializeClass(PlonePopollZODBBackend)
InitializeClass(PlonePopollZSQLBackend)
