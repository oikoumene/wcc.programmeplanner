from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from wcc.programmeplanner.content.programmeplanner import IProgrammePlanner
import datetime

class ProgrammeDates(grok.GlobalUtility):
    grok.name('wcc.programmeplanner.programme_dates')
    grok.implements(IVocabularyFactory)

    _terms = [{
        'value': 'termvalue',
        'title': 'Term Title',
        'token': 'termtoken',
    }]

    def __call__(self, context):
        if not IProgrammePlanner.providedBy(context):
            return SimpleVocabulary()

        terms = []

        days = (context.endDate - context.startDate).days

        dates = [
            context.startDate + datetime.timedelta(days=x) for x in (
                range(days + 1)
            )
        ]

        for date in dates:
            terms.append(SimpleTerm(
                value=date.strftime('%Y-%m-%d'), 
                title=date.strftime('%d %B')
            ))
        return SimpleVocabulary(terms)

