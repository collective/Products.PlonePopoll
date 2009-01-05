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
DEPRECATED Installation module for PlonePopoll
This module remains for documentation purpose only.
It will be removed in the future.
"""
# $Id: Install.py 57510 2008-01-23 13:34:01Z glenfant $

__docformat__ = 'restructuredtext'

# Python imports
from StringIO import StringIO
try:
   from persistent.mapping import PersistentMapping
except ImportError:
   from Persistence import PersistentMapping

# CMF imports
from Products.CMFCore.utils import getToolByName

# AT imports
from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

# Product imports
from Products.PlonePopoll.config import *

tool = 'PlonePopoll Tool'
import sys

def setupCustomSlots(self, out):
   """ sets up the custom slots"""
   #use the right zpt

   popoll_slot = 'here/popoll_slot/macros/popollBox'
   popoll_slot2 = 'here/popoll_slot2/macros/popollBox'
   popoll_portlet = 'here/portlet_popoll/macros/portlet'
   if hasattr(self, "right_slots"):
       right_slots_list=list(self.right_slots)
       if  popoll_slot in right_slots_list:
            self._delProperty('right_slots')
            right_slots_list.remove(popoll_slot)
            self._setProperty('right_slots',tuple(right_slots_list),'lines')
            out.write("Old right slot '%s' has been removed" % popoll_slot)
       elif popoll_slot2 in right_slots_list:
            self._delProperty('right_slots')
            right_slots_list.remove(popoll_slot2)
            self._setProperty('right_slots',tuple(right_slots_list),'lines')
            out.write("Old right slot '%s' has been removed\n" % popoll_slot2)
       if popoll_portlet in right_slots_list:
          out.write("Right slot for popoll exists already\n")
       else:
          self._delProperty('right_slots')
          right_slots_list.append(popoll_portlet)
          self._setProperty('right_slots',tuple(right_slots_list),'lines')
          out.write("Added right slot for popoll\n")



def setupTools(self, out):
    addTool = self.manage_addProduct[PROJECTNAME].manage_addTool
    found = 0
    for obj in self.objectValues():
        if obj.meta_type == tool:
            found = 1

    if found:
        PlonePopollTool = getToolByName(self, TOOL_ID)
        backend = PlonePopollTool.getBackend()
        doMigration(self, backend)
        out.write("Migration to PlonePoll -multiple choice edition- successful.\n")

    if not found:
        addTool(tool, None)
        self.portal_popoll.manage_addProduct[PROJECTNAME].manage_addPlonePopollZODBBackend()
        out.write("Added '%s' tool.\n" % (tool,))


def DEPRECATED_install(self):
    out = StringIO()

    sys.modules['Products.PlonePopoll.PlonePopoll'] = sys.modules['Products.PlonePopoll.content.PlonePopoll']

    # install types
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out, typeInfo, PROJECTNAME)

    # install skin
    install_subskin(self, out, GLOBALS)

    # Install portlet
    setupCustomSlots(self, out)

    # Add portal types to use portal factory
    portal_factory = getToolByName(self, 'portal_factory')
    if portal_factory is not None:
        factoryTypes = list(portal_factory.getFactoryTypes().keys())
        factoryTypes.append('PlonePopoll')
        portal_factory.manage_setPortalFactoryTypes(listOfTypeIds = factoryTypes)
    else:
        out.write('Couldn\'t get Portal Factory, so couldn\'t add PlonePopoll type to it\n')


    # Install tool
    setupTools(self, out)

    install_configlet(self, out)

    provider = getToolByName(self, 'portal_selenium', None)
    if provider:
        # Functional Tests
        action = {'id':PROJECTNAME.lower(),
                  'name':PROJECTNAME,
                  'action':'string:here/get_%s_ftests'%PROJECTNAME.lower(),
                  'condition': '',
                  'permission': 'View',
                  'category':'ftests',
                  'visible': 1}
        provider.addAction(**action)

    typesTool = getToolByName(self, 'portal_types')
    # Set the human readable title explicitly
    t = getattr(typesTool, 'PlonePopoll', None)
    if t:
        t.title = 'Poll'

    # Hide Polls from the navtree
    ntp = getToolByName(self, 'portal_properties').navtree_properties
    bl = list(ntp.getProperty('metaTypesNotToList', ()))
    if 'PlonePopoll' not in bl:
        bl.append('PlonePopoll')
        ntp._p_changed = 1
        ntp.metaTypesNotToList = bl

    migratePopollConfiguration(self, out)

    #raise "Installation OK"
    out.write('Installation completed.\n')
    return out.getvalue()

def install_configlet(self, out):
    try:
        portal_conf=getToolByName(self,'portal_controlpanel')
    except AttributeError:
        print >>out, "Configlet could not be installed"
        return
    try:
        portal_conf.registerConfiglet(**prefs_plonepopoll_configlet)
    except KeyError:
        pass # Get KeyError when registering duplicate configlet.

def DEPRECATED_uninstall(self):
    out = StringIO()

    # remove the configlet from the portal control panel
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        configTool.unregisterConfiglet(CONFIGLET_ID)
        out.write('Removed PlonePopoll configlet\n')

    uninstall_tool(self, out)

    #remove portlet from list
    portlet_popoll = 'here/portlet_popoll/macros/portlet'
    if hasattr(self, 'right_slots'):
        current = list(self.getProperty('right_slots'))
        if portlet_popoll in current:
            current.remove(portlet_popoll)
        self.manage_changeProperties(**{'right_slots' : current})

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()

def uninstall_tool(self, out):
    try:
        self.manage_delObjects([TOOL_ID])
    except:
        pass
    else:
        print >>out, "PlonePopoll tool removed"

def doMigration(self, backend):
    """
   #Migrate Results of PlonePopoll 2.0x or lower to 2.1
   #In version 2.0x or lower : choice of user was stored as Integer
   #In version 2.1 : choice of user is stored as a list of choice
   #Get all results in PlonePopollBackend and change the type of stored choice
    """


    msg = ''
    storedResults = backend._getResults()

    #add if non existant
    if not hasattr(backend.aq_explicit, '_internal_version'):
        backend.aq_explicit._internal_version = 0
    #do changes for 2.0x to 2.1
    if backend.aq_explicit._internal_version < 1:
        backend.aq_explicit._internal_version = 1
        for poll_id in storedResults:
             for user in storedResults[poll_id]:
                choices = storedResults[poll_id][user]
                if not type(choices) == type([]):
                     storedResults[poll_id][user] = [choices]
        backend._results = storedResults
        msg = msg + '\nInternal version set to 1.'
    msg = msg + '\nMigration done.'
    return msg

def migratePopollConfiguration(self, out):
    """
    Migrate simple configuration (one string with portlet selection mode) with
    PersistentMapping
    """
    tool = getToolByName(self, TOOL_ID, None)
    if tool is not None:
        oldconf = getattr(tool, 'portlet_configuration', 'newest')
        if isinstance(oldconf, str):
            # not yet migrated
            configuration = PersistentMapping()
            configuration['selection_mode'] = oldconf
            configuration['number_of_polls'] = 1
            setattr(tool, 'portlet_configuration', configuration)
            out.write('Configration migrated to PersistentMapping')
    return
