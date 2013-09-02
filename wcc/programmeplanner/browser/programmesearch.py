from five import grok
from Products.CMFCore.interfaces import IContentish
from dateutil.parser import parser as dateparser
from DateTime import DateTime

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
            return list(sorted(results, key=lambda x:x.start))

        for date in dates:
            ds = DateTime('%s 00:00' % date)
            de = DateTime('%s 23:59' % date)
            p = params.copy()
            p['start'] = {'query': (ds, de), 'range': 'min:max'}
            brains = self.context.portal_catalog(**p)
            for brain in brains:
                if brain.getPath() in [
                    r.getPath() for r in results]:
                    continue
                results.append(brain)

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
