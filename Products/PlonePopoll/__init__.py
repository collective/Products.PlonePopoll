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
PlonePopoll product
"""
# $Id: __init__.py 53954 2007-11-15 22:11:24Z zegor $

__docformat__ = 'restructuredtext'

import logging

from AccessControl.Permissions import view_management_screens
# Zope imports
from zope.i18nmessageid import MessageFactory

# CMF imports
from Products.CMFCore.DirectoryView import registerDirectory

from Products.CMFCore.utils import ContentInit, ToolInit

# AT imports
from Products.Archetypes.public import process_types, listTypes

# Product import
from Products.PlonePopoll.config import *

logger = logging.getLogger(PROJECTNAME)
PopollMessageFactory = MessageFactory(I18N_DOMAIN)

from Products.PlonePopoll.content import *
from Products.PlonePopoll.PlonePopollTool import *
from Products.PlonePopoll.PlonePopollBackend import *


registerDirectory(SKINS_DIR, GLOBALS)

# Initialization method
def initialize(context):
    listOfTypes = listTypes(PROJECTNAME)
    content_types, constructors, ftis = process_types(listOfTypes, PROJECTNAME)

    ContentInit(PROJECTNAME + ' Content',
                content_types      = content_types,
                permission         = PlonePopoll_addPermission,
                extra_constructors = constructors,
                fti                = ftis,
    ).initialize(context)

    ToolInit('%s Tool' % PROJECTNAME,
             tools        = (PlonePopollTool,),
             icon         = 'tool.gif',
    ).initialize(context)


    # This has to be improved so that only PlonePopollManager objects can hold PlonePopollBackends
    # and PlonePopollBackends can be derived.
    context.registerClass(
        PlonePopollZODBBackend,
        permission=view_management_screens,
        constructors=(manage_addPlonePopollZODBBackend,),
        visibility=None,
        icon='www/PlonePopollBackend.gif',
        )

    context.registerClass(
        PlonePopollZSQLBackend,
        permission=view_management_screens,
        constructors=(manage_addPlonePopollZSQLBackend,),
        visibility=None,
        icon='www/PlonePopollBackend.gif',
        )
