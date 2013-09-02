from collective.grok import gs
from wcc.programmeplanner import MessageFactory as _

@gs.importstep(
    name=u'wcc.programmeplanner', 
    title=_('wcc.programmeplanner import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.programmeplanner.marker.txt') is None:
        return
    portal = context.getSite()
    portal.portal_catalog.reindexIndex('event_type', portal.REQUEST)
    portal.portal_catalog.reindexIndex('focus_group', portal.REQUEST)
    # do anything here
