from five import grok
from Products.CMFCore.interfaces import IContentish
from dateutil.parser import parser as dateparser

grok.templatedir('templates')

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

        event_type = self.request.get('event_type', '')
        if event_type:
            params['wcc_event_type'] = event_type

        results = set()

        dates = self.request.get('dates', [])
        for date in dates:
            dt = dateparser(date)
            p = params.copy()
            p['start'] = date
            brains = self.context.portal_catalog(**params)
            for brain in brains:
                results.add(brain)

        return list(sorted(results, key=lambda x:x.start))

    def results(self):
        results = []
        for b in self._raw_results():
            o = b.getObject()
            item = {
                'day': o.startDate.strftime('%A %d %B %Y'),
                'schedule': '%s - %s' % (
                    o.startDate.strftime('%r'),
                    o.endDate.strftime('%r')
                ),
                'event_type': getattr(o, 'event_type', ''),
                'title': o.Title(),
                'description': o.Description()
            }
            results.append(item)

        return results
