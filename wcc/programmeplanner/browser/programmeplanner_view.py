from five import grok
from plone.directives import dexterity, form
from wcc.programmeplanner.content.programmeplanner import IProgrammePlanner
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IProgrammePlanner)
    grok.require('zope2.View')
    grok.template('programmeplanner_view')
    grok.name('view')

    def event_types(self):
        factory = getUtility(IVocabularyFactory, name='wcc.programmeplanner.event_type')
        return factory(self.context)

    def focus_groups(self):
        factory = getUtility(IVocabularyFactory, name='wcc.programmeplanner.focus_group')
        return factory(self.context)

    def dates(self):
        factory = getUtility(IVocabularyFactory,
                name='wcc.programmeplanner.programme_dates')
        return factory(self.context)
