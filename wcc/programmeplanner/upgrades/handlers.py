from collective.grok import gs
from Products.CMFCore.utils import getToolByName

# -*- extra stuff goes here -*- 


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
        obj.reindexObject()
