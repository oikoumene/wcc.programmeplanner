from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource

class EventType(grok.GlobalUtility):
    grok.name('wcc.programmeplanner.event_type')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': 'madang-workshop',
        'title': 'Madang Workshop',
        'token': 'madang-workshop',
    },{
        'value': 'madang-performance',
        'title': 'Madang Performance',
        'token': 'madang-performance',
    },{
        'value': 'bible-study-prayer',
        'title': 'Bible Study / Prayer',
        'token': 'bible-study-prayer',
    },{
        'value': 'ecumenical-conversation',
        'title': 'Ecumenical Conversation',
        'token': 'ecumenical-conversation',
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(*i))
        return SimpleVocabulary(terms)
