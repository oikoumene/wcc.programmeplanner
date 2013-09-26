from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from wcc.programmeplanner import MessageFactory as _

class FocusGroup(grok.GlobalUtility):
    grok.name('wcc.programmeplanner.focus_group')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': 'inter-religious',
        'title': _('Inter-religious'),
    },{
        'value': 'gender',
        'title': _('Gender'),
    },{
        'value': 'indigenous-people',
        'title': _('Indigenous People'),
    },{
        'value': 'youth',
        'title': _('Youth'),
    }]

    def __call__(self, context):
        terms = []
        for i in self._terms:
            terms.append(SimpleTerm(**i))
        return SimpleVocabulary(terms)
