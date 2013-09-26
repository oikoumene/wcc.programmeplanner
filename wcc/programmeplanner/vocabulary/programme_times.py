from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource

class ProgrammeTimes(grok.GlobalUtility):
    grok.name('wcc.programmeplanner.programme_times')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        items = [
            '8:30',
            '9:15',
            '10:45',
            '14:15',
            '16:15',
            '18:15',
            '20:00'
        ]
        terms = [SimpleTerm(i, i, i) for i in items]
        return SimpleVocabulary(terms)
