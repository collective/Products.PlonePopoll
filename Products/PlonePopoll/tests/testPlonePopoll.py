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

# $Id: testPlonePopoll.py 49710 2007-09-19 16:24:47Z glenfant $

from Products.PlonePopoll.content import *
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase import PloneTestCase
PloneTestCase.installProduct('PlonePopoll')

PloneTestCase.setupPloneSite(products=['PlonePopoll'])


def sortTuple(t):
    l = list(t)
    l.sort()
    return tuple(l)

class TestPlonePopoll(PloneTestCase.PloneTestCase):

    #utility method

    def createMember(self, id, pw, email, roles=('Member',)):
        ptool = getToolByName(self.portal, 'portal_registration')
        member = ptool.addMember(id, pw, roles, properties={ 'username': id, 'email' : email })
        self.mbtool.createMemberArea(id)
        return member

    def createGroup(self, id):
        pgroup = getToolByName(self.portal, 'portal_group')
        pgroup.addGroup(id, '', (), ())
        return pgroup.getGroupById(id)

    def installPlonePopoll(self):
        #self.loginAsPortalOwner()
        self.qi =  getToolByName(self.portal, 'portal_quickinstaller')
        self.qi.installProduct('PlonePopoll')

    def setupSecurityContext(self):
        self.logout()
        self.loginAsPortalOwner()


        #create a bunch of users
        self.user1 = self.createMember('user1', 'abcd4', 'abc@domain.tld')
        self.createMemberarea('user1')
        self.user2 = self.createMember('user2', 'abcd4', 'abc@domain.tld')
        self.createMemberarea('user2')
        self.user3 = self.createMember('user3', 'abcd4', 'abc@domain.tld')
        self.createMemberarea('user3')
        """
        self.failUnless('user1' in self.portal.Members.objectIds())
        self.failUnless('user2' in self.portal.Members.objectIds())
        self.failUnless('user3' in self.portal.Members.objectIds())
        """
        #just in case ...
        self.logout()
        self.login('user1')
        self.folder = self.mbtool.getHomeFolder()

    def afterSetUp(self, ):
        #some usefull properties
        """
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.membership = self.portal.portal_membership
        """
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.mbtool = getToolByName(self.portal, 'portal_membership')

        #install product
        #self.installPlonePopoll()

        #setup users and groups
        self.setupSecurityContext()


    def createPopoll(self, id="sample_poll", folder= None):
        # Login
        self.login("user1")
        if not folder:
            folder = self.mbtool.getHomeFolder('user1')

        # Content creation
        content_id = id
        folder.invokeFactory(
            type_name = 'PlonePopoll',
            id = content_id
        )

        self.failUnless(content_id in folder.objectIds(), "Object has not been created or not with the right id")
        content = getattr(folder, content_id)

        return content

    def changePollOptions(self, poll, question='', choices=[], choices_number=1):
        poll.setPollOptions(
                question = question,
                choices = choices,
                choices_number = choices_number,
        )
        self.assertEqual(poll.getPollNumber(), choices_number)
        self.assertEqual(poll.getChoices(), choices)
        self.assertEqual(poll.getQuestion(), question)

    def editPopoll(self, poll, _title="", _question="", _answers=[], _poll_status= True, _number=1, _results_visibility= True):
        """
        Edit poll with default params
        """
        poll.edit(
            title=_title,
            )
        self.assertEqual(poll.Title(), title)
        self.assertEqual(poll.getQuestion(), question)
        self.assertEqual(poll.isEnabled(), poll_status)
        self.assertEqual(poll.getPollNumber(), number)
        self.assertEqual(poll.isVisible(), results_visibility)




    def test_00_createPopoll(self):
        """
        Create new poll in home directory & check its basic properties and behaviour
        """
        # Create poll
        content_id = "my_popoll"
        content = self.createPopoll(content_id)

        # Basic checks
        self.assertEqual(content.Title(), '')
        self.assertEqual(content.getId(), content_id)
        return


    def test_01_setPopoll(self):
        """
        Set poll options
        """
        # Create poll and test that initial options are set correctly
        popoll = self.createPopoll()
        self.failUnless(popoll.getQuestion() == "", )

        self.failUnless(popoll.getChoices() == (), )

        # Set popoll options
        popoll.setPollOptions(
            question = "QUESTION",
            choices = [
            "A",
            "B",
            "C",
            "D",
            ],
            )

        # Ensure that they are applied
        self.failUnless(popoll.getQuestion() == "QUESTION")
        self.failUnless(popoll.getChoices() == ("A", "B", "C", "D", ))

        # Reset popoll options
        popoll.setPollOptions(
            question = "QUESTION2",
            choices = [
            "A2",
            "B2",
            "C2",
            "D2",
            ],
            )

        # Ensure that they are applied
        self.failUnless(popoll.getQuestion() == "QUESTION2")
        self.failUnless(popoll.getChoices() == ("A2", "B2", "C2", "D2", ),
                        "Choices are invalid (%s)" % str(popoll.getChoices()))

    def test_02_voting(self):
        """
        Vote for an option
        """
        # Set popoll options
        popoll = self.createPopoll()
        popoll.setPollOptions(
                    question = "QUESTION",
                    choices = ["A","B","C","D",])

        # (enable and) Voooote !
        popoll.setEnabled(True)
        popoll.vote(choices = [ 0 ] )

        # Check results.
        # getResults returns a LIST of DICTS with the following keys :
        #        index, label, votes, percentage
        self.failUnless(popoll.getVotesCount() == 1,
                        "Invalid number of votes taken into consideration (%d instead of 1)" % (popoll.getVotesCount()))
        dict = popoll.getResults()[0]
        ## self.failUnless(dict["index"] == 0, "Invalid option index when returning results")
        ## self.failUnless(dict["label"] == "A", "Invalid option label when returning results")
        ## self.failUnless(dict["votes"] == 1, "Invalid number of votes when returning results")
        ## self.failUnless(dict["percentage"] == 1, "Invalid percentage when returning results")


    def test_03_mass_voting(self):
        """
        Test mass voting
        """
        # set first popoll
        poll1 = self.createPopoll("poll1")
        poll1.setPollOptions(
            question = "Uh ?",
            choices = ["1", "2", "3", "Nous irons aux bois", ],
            check_multi = 0,
            )
        poll2 = self.createPopoll("poll2")
        poll2.setPollOptions(
            question = "Bah alors ?",
            choices = ["4", "5", "6", "Cueillir des cerises", ],
            check_multi = 0,
            )
        poll1.setEnabled(True)
        poll2.setEnabled(True)

        # Vote
        poll1.vote(choices = [ 0,1,2,3 ])
        poll2.vote(choices = [ 3,1,0,3,1 ])

        # Compute tests results
        self.failUnless(poll1.getVotesCount() == 4, "Invalid number of votes taken into consideration (%d instead of 4)" % (poll1.getVotesCount()))
        self.failUnless(poll2.getVotesCount() == 5, "Invalid number of votes taken into consideration (%d instead of 5)" % (poll2.getVotesCount()))
        self.failUnless(poll1.getResults()[0][2] == 25, "Results percentage is %f instead of 25" % (poll1.getResults()[0][2], ))




    def test_04_vote_enabling(self):
        """
        Test if it is possible to vote when it is enabled or not
        """
        poll1 = self.createPopoll("poll1")
        poll1.setPollOptions(
            question = "Bah alors ?",
            choices = ["4", "5", "6", ]
            )

        # A poll is enabled by default
        poll1.setEnabled(False)

        try:
            poll1.vote([2])
        except:
            pass
        else:
            self.fail("It should not be possible to vote when a poll is disabled")

        poll1.setEnabled(True)
        poll1.vote([2])

        poll1.setEnabled(False)
        try:
            poll1.vote([2])
        except:
            pass
        else:
            self.fail("It should not be possible to vote when a poll is disabled")

    def test_05_single_choice_vote(self):
        # Non-multi-vote behaviour
        question = 'une question ?'
        choices = ('answer1', 'answer2', 'answer3')
        poll2 = self.createPopoll("poll2")

        self.changePollOptions(
                        poll=poll2,
                        question = question,
                        choices = choices,
                        choices_number = 1,
        )
        poll2.setEnabled(True)
        self.login("user2")
        #TO CHANGE
        # it is the interface that is testing how much vote are to keep, has to changed
        user_choice = 0
        if poll2.hasVoted():
            poll2.removeUserVote()
        poll2.vote( [int(user_choice),])

        #one person has voted
        self.assertEqual(poll2.getPersonVoteCount(), 1)
        #there is only one vote
        self.assertEqual(poll2.getVotesCount(), 1)

        #finally the last vote should be saved, it is for choice 0
        choice = poll2.getResults()[0]
        choice_id = choice[0];
        choice_count = choice[1];
        choice_percentage = '%0.2f'%choice[2];
        #verify vote (first choice)
        self.assertEqual(choice_count, 1)
        self.assertEqual(choice_percentage, '100.00')

        choice = poll2.getResults()[1]
        choice_id = choice[0];
        choice_count = choice[1];
        choice_percentage = '%0.2f'%choice[2];
        #verify vote (second choice)
        self.assertEqual(choice_count, 0)
        self.assertEqual(choice_percentage, '0.00')

    def test_05_multi_choice_vote(self):
        """
        Test if a user cannot vote several times when multi-vote is checked against
        """


        # Multi-vote behaviour (default behaviour)
        poll1 = self.createPopoll("poll1")
        question = "Bah alors ?"
        choices = ("4", "5", "6")

        self.changePollOptions(
                        poll=poll1,
                        question = question,
                        choices = choices,
                        choices_number = 2,
        )
        poll1.setEnabled(True)

        self.login("user2")
        poll1.vote( [0, 1] )

        #one person has voted
        self.assertEqual(poll1.getPersonVoteCount(), 1)

        #total vote must be 2
        self.assertEqual(poll1.getVotesCount(), 2)

        choice = poll1.getResults()[0]
        choice_id = choice[0];
        choice_count = choice[1];
        choice_percentage = '%0.2f'%choice[2];
        #verify vote (first choice)
        self.assertEqual(choice_count, 1)
        self.assertEqual(choice_percentage, '50.00')

        choice = poll1.getResults()[1]
        choice_id = choice[0];
        choice_count = choice[1];
        choice_percentage = '%0.2f'%choice[2];
        #verify vote (second choice)
        self.assertEqual(choice_count, 1)
        self.assertEqual(choice_percentage, '50.00')


    def test_06_folder_poll(self):
        """
            test if we can get the published poll in local folder appears first
        """
        poll1 = self.createPopoll("poll1")

    def test_07_clone_poll(self):
        """
            BUG of copy a poll
            when a poll is copied the uiid has to be different for the copied version
        """
        self.login('user1')
        src = self.mbtool.getHomeFolder('user1')

        poll = self.createPopoll(id="popoll_copy", folder=src)
        dest = self.mbtool.getHomeFolder('user1')
        dest.invokeFactory(type_name = 'Folder', id = 'copy')
        dest = getattr(dest, 'copy')
        dest.manage_pasteObjects(src.manage_copyObjects('popoll_copy'))

        # After a copy/paste, they should *both* have a copy
        self.failUnless(hasattr(aq_base(src), 'popoll_copy'))
        self.failUnless(hasattr(aq_base(dest), 'popoll_copy'))

        poll_copy = getattr(aq_base(dest), 'popoll_copy')
        self.failIf(poll_copy.getVoteId() == poll.getVoteId(), 'A copied poll must have a new generated uid.')

    """
    #won't work so, it the backend that change its storage not the popoll
    def test_06_migration(self, ):
        self.folder._importObjectFromFile('poll_v2_0x.zexp')
        poll = getattr(self.folder, 'poll_v2_0x')
        choice = poll.getResults()[0]
        choice_id = choice[0];
        choice_count = choice[1];

        poll.getResults()[1][1]
        # do reinstall to migrate
        self.installPlonePopoll()
        poll.getResults()[1][1]
    """

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPlonePopoll))
    return suite
