Changelog
=========

2.8b3 (2018-03-09)
------------------

- Translated some untranslated strings into Dutch, German and French.
  [khink]


2.8b2 (2018-03-01)
------------------

- Remove pseudo-field ``contentDescription`` and its use in Poll view.
  [khink]

- Fix a selection bug when your choice is greater than 10.
  [boulch]

- Add minimal buildout
  [bsuttor]

- Include permission from Products.CMFCore for fixing zcml error
  [bsuttor]

- Accessibility fix: text node replaced with HTML label
  [keul]

- Do not raise Unauthorized error anymore is user can see
  the Poll but not vote
  [keul]

- Description field is now displayed
  [keul]

- Do not filter Popoll in portlet for anonymous (close `#1`__)
  [micecchi, keul]

- Some additional user messages in the Poll view
  [keul]

- Restored natural Plone order for field in the Poll view
  [keul]

- Fixed Poll view for Plone 4 compatibility
  [cekk]

__ https://github.com/collective/Products.PlonePopoll/issues/1

2.8b1 (2013-03-05)
------------------
* Fixed italian translation (micecchi)
* Moved repo to Plone github collective [sneridagh]
* Plone 4.3 support [sneridagh]

2.7.3b1 (2010-05-05)
----------------------

* Fix malformed HTML entities. (kdeldycke)
* Plone4 support: drop the usage of the deprecated PTSTranslationDomain (jcbrand)

2.7.1
-----

* Added a catalog index in GS profile (isEnabled) to make poll portlet working
  (disabled polls must not be displayed)

2.7.0-beta2
-----------

* Popoll is now an egg (macadames)
* Fix french translation (vote is not feminine in french - stop scraping popoll) (macadames)

2.7.0-beta1
-----------

* Fixed deprecated stuffs (for Zope 2.10/Plone 3) (glenfant)
* GenericSetup installation (Install.py deprecated) (glenfant)
* Made code more simple. (glenfant)
* Plone 3 style portlet replaces the config panel. (glenfant)
* Multi-colors bars for results (zegor)
* Updated french translation, zpt and css (zegor)
* Fixed a bug that prevent to view results after voting when showing results
  in forms is not activated. (zegor)
* Translations cleanup (.pot) (zegor)

2.6.1 - SVN
-----------

* added french translations
* it is not possible to vote again on plonepopoll_view page;
  cleanup (naro)
* added new poll option - showCurrentResults - this option (boolean
  field) allows to display current poll results before user
  vote. Switched off by default. (naro)
* It is possible to display more than one poll in the portlet. Number
  of polls is set in the Poll tool settings. (naro)
* Translators should check updated msgids:
  *label_portlet_configuration_newest*,
  *label_portlet_configuration_branch*,
  *label_portlet_configuration_subbranches*. (naro)
* synced all translations (naro)
* slightly refactored PlonePopoll_getPortletPoll script to reflect new
  configuration storage settings (naro)
* fixed 'branch' configuration mode (returned list of lists instead of list) (naro)
* Added czech translation by Lukas Zdych
* Allow skinnable corners

2.5.1 - (2006-02-08)
--------------------

* Restructure polls_list for Plone 2.1 and 2.5 compatibility
* Restructured portlet_popoll for Plone 2.1 and 2.5 compatibility (ferri)
* Added _at_rename_after_creation property in poll class (ferri)
* i18n fixes (ferri)
* General cleaup (ferri)

2.5 - (2006-24-03)  - CVS
-------------------------

* Updated for Archetypes
* Added greek translation thanks to Menelaos Maglis
* added show_id method to PlonePopoll for forward compatability to Plone 2.
* Fixed ZODB transaction on every anonymous request - (zegor)

2.4 - (2005-12-05)
------------------

* Use toLocalizedTime
* Added FTests
* Removed superfluous answers2text.py
* Don't loose answers when error
* Error handling for answers
* Number of choices field after answers field!
* Poll enabled by default
* Newest poll as default
* Work on the i18n files. Only fr, de and en are now fully up to date.
* Integrated nl translation, thanks to Michael Reitsma
* Removed some debugging code in polls2.pt that was hidden in HTML
  comments and called resultObject.aq_explicit.aq_parent.aq_parent.Type(),
  but no Type method was found.
* Make Installation work with Plone 2.1
* Move permission installation from Install.py to Permissions.py
* Move Permissions to Permissions.py
* Install doesn't call setupMessageCatalog any more because it doesn't
  work with Plone 2.1.
* polls2 : remove the displaying of the container type
* translation changes (de, es)

2.3 - (2005-02-04)
------------------

* Fixed the test on the number of choices
* Fixed a cache bug in ZODB

2.1 - (20040-06-16)
-------------------

* Multiple choice authorized for one poll

2.0 - (2004-03-23)
------------------

* Plone 2.0 support
* Clear button to clear poll votes

2.0Beta1 - (2003-12-18)
-----------------------

* Plone2.0 support

1.0 - (2003-12-05)
------------------

* Fixed ZODB pb.
* Minor cosmetic changes

0.3 - (2003-05-14)
------------------

* Added I18N install automation support

0.0 - (2003-04-17)
------------------

* Bugfix : Made getUnicityFactor Plone-user compliant : the same Plone
  user cannot vote (distinctly) several times.

