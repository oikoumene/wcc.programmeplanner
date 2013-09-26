from five import grok
from Products.CMFCore.interfaces import IContentish
from dateutil.parser import parser as dateparser
from DateTime import DateTime
import time
import dateutil.tz
import datetime
from zope.component.hooks import getSite

grok.templatedir('templates')

def get_timezone():
    localtz = dateutil.tz.tzlocal()
    localoffset = localtz.utcoffset(datetime.datetime.now())
    return (localoffset.days * 86400 + localoffset.seconds) / 3600

def time_more_than(a, b):
    z, x = a.split(':')
    n, m = b.split(':')
    if int(z) > int(n):
        return True
    if int(z) == int(n) and int(x) >= int(m):
        return True
    return False

class ProgrammeSearch(grok.View):
    grok.context(IContentish)
    grok.name('programmesearch')
    grok.require('zope2.View')
    grok.template('programmesearch')

    def _raw_results(self):
        params = {
            'portal_type':'wcc.programmeplanner.programme',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 5
            }
        }

        search = self.request.get('search', '')
        if search:
            params['SearchableText'] = search

        event_type = self.request.get('event_type', '').strip()
        if event_type and event_type != 'all':
            params['event_type'] = event_type


        focus_group = self.request.get('focus_group', '').strip()
        if focus_group and focus_group != 'all':
            params['focus_group'] = focus_group

        results = []

        dates = self.request.get('dates', [])
        if not dates:
            results = self.context.portal_catalog(**params)

        tz = get_timezone()
        for date in dates:
            ds = DateTime('%s 00:00 GMT%+d' % (date, tz))
            de = DateTime('%s 23:59 GMT%+d' % (date, tz))
            p = params.copy()
            p['start'] = {'query': (ds, de), 'range': 'min:max'}
            brains = self.context.portal_catalog(**p)
            for brain in brains:
                if brain.getPath() in [
                    r.getPath() for r in results]:
                    continue
                results.append(brain)

        start_time = self.request.get('start_time', '').strip()
        if start_time and start_time != 'all':
            results = [i for i in results if time_more_than(
                i.getObject().startTime, start_time)]

        return list(sorted(results, key=lambda x:x.start))

    def results(self):
        results = []
        for b in self._raw_results():
            o = b.getObject()
            item = {
                'day': o.date.strftime('%A %d %B %Y'),
                'schedule': '%s - %s' % (
                    o.startTime,
                    o.endTime
                ),
                'event_type': getattr(o, 'event_type', ''),
                'title': o.Title(),
                'description': o.Description(),
                'url': o.absolute_url()
            }
            results.append(item)

        return results


    def event_type_icon(self, event_type):
        site = getSite()
        return '%s/++resource++wcc.programmeplanner/images/%s-icon.png' % (
            site.absolute_url(), 
            event_type
        )

