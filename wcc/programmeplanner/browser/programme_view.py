from five import grok
from plone.directives import dexterity, form
from wcc.programmeplanner.content.programme import IProgramme

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IProgramme)
    grok.require('zope2.View')
    grok.template('programme_view')
    grok.name('view')

