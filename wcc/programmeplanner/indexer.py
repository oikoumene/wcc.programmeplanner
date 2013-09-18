from plone.indexer import indexer
from wcc.programmeplanner.content.programme import IProgramme
from DateTime import DateTime
import time
from dateutil.parser import parse as parse_date

@indexer(IProgramme)
def programme_start(obj):
#    tzone = time.timezone/3600
#    return DateTime('%s %s GMT%+d' % (obj.date, obj.startTime, tzone))
    return parse_date('%s %s' % (
        obj.date.strftime('%Y-%m-%d'),
        obj.startTime
        )
    )

@indexer(IProgramme)
def programme_end(obj):
#    tzone = time.timezone/3600
#    return DateTime('%s %s GMT%+d' % (obj.date, obj.endTime, tzone))
    return parse_date('%s %s' % (
        obj.date.strftime('%Y-%m-%d'),
        obj.endTime
        )
    )
