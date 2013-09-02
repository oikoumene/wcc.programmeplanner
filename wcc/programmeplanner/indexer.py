from plone.indexer import indexer
from wcc.programmeplanner.content.programme import IProgramme

@indexer(IProgramme)
def programme_start(obj):
    return obj.startDate

@indexer(IProgramme)
def programme_end(obj):
    return obj.endDate
