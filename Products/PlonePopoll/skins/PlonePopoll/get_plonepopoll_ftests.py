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

## Script (Python) "get_plonepopoll_ftests"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
selenium = context.portal_selenium
suite = selenium.getSuite()
target_language='en'
suite.setTargetLanguage(target_language)

selenium.addUser(id = 'sampleadmin',fullname='Sample Admin',roles=['Member', 'Manager',])
selenium.addUser(id = 'samplemember',fullname='Sample Member',roles=['Member',])

test_logout = suite.TestLogout()
test_admin_login  = suite.TestLoginPortlet('sampleadmin')
test_member_login  = suite.TestLoginPortlet('samplemember')
test_switch_language = suite.TestSwitchToLanguage()

plone21 = selenium.getPloneVersion() > "2.0.5"
plone25 = selenium.getPloneVersion() >= "2.5"

if plone21:
    delete_from_folder = "/folder_delete?paths:list=" + suite.getTest().base + '/'
else:
    delete_from_folder = "/folder_delete?ids:list="

suite.addTests("PlonePopoll",
    'Login as Sample Admin',
    test_admin_login,
    test_switch_language,
    'Admin adds Poll',
    suite.open(delete_from_folder + 'plonepoll'),
     suite.open("/"),
    suite.clickAndWait( "link=View"),
    suite.clickAndWait( "link=Poll"),
    suite.verifyTextPresent("Poll has been created."),
    suite.type("name=id","plonepoll"),
    suite.clickAndWait("name=form.button.Save"),
    suite.verifyTextPresent("Please correct the indicated errors."),
    suite.verifyTextPresent("At least two answers are needed for the Poll."),
    suite.type("name=title","Opinion Poll"),
    suite.type("name=question","What is your opinion?"),
    suite.clickAndWait("name=form.button.Save"),
    suite.verifyTextPresent("Please correct the indicated errors."),
    suite.verifyTextPresent("At least two answers are needed for the Poll."),
    suite.type("name=answers:lines","Answer 1<br />Answer 2<br />Answer 3"),
    suite.type("name=number","0"),
    suite.clickAndWait("name=form.button.Save"),
    suite.verifyTextPresent("Number of possible choices must be between one and the number of answers."),
    suite.type("name=number","4"),
    suite.clickAndWait("name=form.button.Save"),
    suite.verifyTextPresent("Number of possible choices must be between one and the number of answers."),
    suite.type("name=number","1"),
    suite.clickAndWait("name=form.button.Save"),
    suite.verifyTextPresent("Poll changes saved."),
    "Admin votes",
    suite.open("/plonepoll"),
     )

return suite
