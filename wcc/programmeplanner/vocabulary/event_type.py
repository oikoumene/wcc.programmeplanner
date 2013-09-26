from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from wcc.programmeplanner import MessageFactory as _

class EventType(grok.GlobalUtility):
    grok.name('wcc.programmeplanner.event_type')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': 'madang-workshop',
        'title': _('Madang workshop'),
    },{
        'value': 'madang-performance',
        'title': _('Madang performance'),
    },{
        'value': 'bible-study',
        'title': _('Bible Study'),
    },{
        'value': 'ecumenical-conversation',
        'title': _('Ecumenical Conversation'),
    },{
        'value': 'prayer',
        'title': _('Prayer')
    },{
        'value': 'plenary',
        'title': _('Plenary')
    },{
        'value': 'other',
        'title': _('Other')
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(**i))
        return SimpleVocabulary(terms)
