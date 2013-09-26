from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
import time

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.programmeplanner to 3',
                description=u'Upgrade wcc.programmeplanner to 3',
                source='2', destination='3',
                sortkey=1, profile='wcc.programmeplanner:default')
def to3(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.programmeplanner.upgrades:to3')


@gs.upgradestep(title=u'Upgrade wcc.programmeplanner to 2',
                description=u'Upgrade wcc.programmeplanner to 2',
                source='1', destination='2',
                sortkey=1, profile='wcc.programmeplanner:default')
def to2(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.programmeplanner.upgrades:to2')

    catalog = getToolByName(context, 'portal_catalog')
    
    brains = catalog({'portal_type': 'wcc.programmeplanner.programme'})

    for brain in brains:
        obj = brain.getObject()
        if isinstance(obj.focus_group, str):
            obj.focus_group = [obj.focus_group]
        if getattr(obj, 'startDate', None):
            if isinstance(obj.startDate, DateTime):
                sd = obj.startDate.asdatetime()
            else:
                sd = obj.startDate
            obj.date = sd.date()
            obj.startTime = sd.strftime('%H:00')
        if getattr(obj, 'endDate', None):
            if isinstance(obj.endDate, DateTime):
                ed = obj.endDate.asdatetime()
            else:
                ed = obj.endDate
            obj.endTime = ed.strftime('%H:00')
        obj.reindexObject()
