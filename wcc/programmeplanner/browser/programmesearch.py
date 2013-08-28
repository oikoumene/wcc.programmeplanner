from five import grok
from Products.CMFCore.interfaces import IContentish
from wcc.programmeplanner.interfaces import IProgrammeSearchCapable

grok.templatedir('templates')

class ProgrammeSearch(grok.View):
    grok.context(IContentish)
    grok.name('programmesearch')
    grok.require('zope2.View')
    grok.template('programmesearch')
