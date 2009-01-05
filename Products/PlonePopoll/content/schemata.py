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
PlonePopoll
"""
# $Id: schemata.py 52252 2007-10-23 14:23:28Z zegor $

__docformat__ = 'restructuredtext'


from Products.ATContentTypes import atct

# Archetypes imports
from Products.Archetypes.public import *

PollSchema = atct.ATContentTypeSchema.copy() + Schema((
    StringField(
        'question',
        required = True,
        widget = StringWidget(
            size=60,
            label            = 'Question',
            label_msgid       = 'label_question',
            description       = 'Enter the Poll question.',
            description_msgid = 'help_question',
            i18n_domain       = 'plonepopoll',
        ),
    ),
    LinesField(
        'choices',
        required   = True,
        widget     = LinesWidget(
            label             = 'Answers',
            label_msgid       = 'label_answers',
            description       = 'Enter each possible answer on one line.',
            description_msgid = 'help_answers',
            i18n_domain       = 'plonepopoll',
        ),
    ),
    IntegerField(
        'number_of_choices',
        default    = 1,
        widget     = IntegerWidget(
            label             = 'Choice count',
            label_msgid       = 'label_choice_count',
            description       = 'Enter the number of choices available.',
            description_msgid = 'help_choice_count',
            i18n_domain       = 'plonepopoll',
        ),
    ),
    BooleanField(
        'visible',
        default    = True,
        accessor   = 'isVisible',
        widget     = BooleanWidget(
            label             = 'Poll Results Visibility',
            label_msgid       = 'label_results_visible',
            description       = 'Select whether you want the Poll results to be visible.',
            description_msgid = 'help_poll_results_visibility',
            i18n_domain       = 'plonepopoll',
        )
    ),
    BooleanField(
        'showCurrentResults',
        default    = False,
        widget     = BooleanWidget(
            label             = 'Show results on vote screen',
            label_msgid       = 'label_poll_show_current_results',
            description       = 'Select whether you want to show current results on vote page or portlet',
            description_msgid = 'help_poll_show_current_results',
            i18n_domain       = 'plonepopoll',
        )
    ),
    BooleanField(
        'enabled',
        default    = True,
        accessor   = 'isEnabled',
        index      = 'FieldIndex',
        widget     = BooleanWidget(
            label             = 'Poll Status',
            label_msgid       = 'label_poll_status',
            description       = 'Select whether you want the Poll to be enabled.',
            description_msgid = 'help_poll_status',
            i18n_domain       = 'plonepopoll',
        )
    ),
))
